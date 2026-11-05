#!/usr/bin/env python3
"""
Compute the state of an initiative from its files: what is done, what is ready to do
next, what is blocked. Session files are not read: they are not committed.

Steps follow the lifecycle in .specify/session/protocol.md. A step is:
  done     its artifact exists and has no unfilled placeholders
  ready    the first step that is not done
  blocked  an earlier step is not done
  skipped  L4 steps when no spec names this initiative and all its requirements are
           already implemented

/speckit-consilium is not a step: it leaves no file. It is listed under next.also_consider
before graduation for Standard and higher.

Usage:
  python tools/scripts/speckit-status.py <INIT> [--root <path>] [--json]

  --json  print one JSON document to stdout. Diagnostics have the form
          {severity, code, message, fix}.

Exit codes:
  0 — state computed
  1 — initiative not found or invalid
"""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

import yaml

MODULE_PATH = Path(__file__).resolve().parent / 'check-spec-quality.py'
SPEC = importlib.util.spec_from_file_location('check_spec_quality', MODULE_PATH)
quality = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(quality)

INITIATIVE_PATTERN = re.compile(r'^INIT-[0-9]{4}-[0-9]{3}-[a-z0-9-]+$')
TERMINAL_STATUSES = {'implemented', 'verified'}
TERMINAL_OR_RETIRED = TERMINAL_STATUSES | {'deprecated'}
CONTRACT_FILES = ('contracts/openapi.yaml', 'contracts/asyncapi.yaml')
L4_STEPS = {'specify', 'plan', 'tasks', 'trace'}
TEMPLATE_TASKS = '.specify/specs/{NNN}-{slug}/tasks.md'


def diagnostic(severity: str, code: str, message: str, fix: str) -> dict:
    return {'severity': severity, 'code': code, 'message': message, 'fix': fix}


class Context:
    """Files of one initiative, with the problems found while reading them."""

    def __init__(self, root: Path, init_dir: Path, name: str, metadata: dict, requirements: list):
        self.root = root
        self.init_dir = init_dir
        self.name = name
        self.metadata = metadata
        self.requirements = requirements
        self.active_requirements = [req for req in requirements if req.get('status') != 'deprecated']
        self.specs = linked_specs(root, name)
        self.diagnostics = []

    def filled(self, path: Path, command: str) -> bool:
        """True if the file exists and has no unfilled placeholders."""
        if not path.is_file():
            return False
        found = quality.find_placeholders(path.read_text(encoding='utf-8'), skip_code_blocks=True)
        if not found:
            return True
        line_no, token = found[0]
        self.diagnostics.append(diagnostic(
            'warning', 'UNFILLED_PLACEHOLDER',
            f"{path.relative_to(self.root)}: {len(found)} unfilled placeholder(s), first at line {line_no}: {{{token}}}",
            f"Fill them with {command}",
        ))
        return False

    def relative(self, path: Path) -> str:
        return str(path.relative_to(self.root))


def linked_specs(root: Path, name: str) -> list:
    """L4 spec directories whose spec.md names this initiative."""
    specs = []
    for spec_md in sorted((root / '.specify' / 'specs').glob('*/spec.md')):
        if '{' not in str(spec_md.parent) and quality.parse_initiative_id(spec_md.read_text(encoding='utf-8')) == name:
            specs.append(spec_md.parent)
    return specs


def trace_rows(path: Path) -> set:
    return set(quality.REQ_ID_PATTERN.findall(path.read_text(encoding='utf-8'))) if path.is_file() else set()


def check_prd(ctx):
    path = ctx.init_dir / 'prd.md'
    return ctx.filled(path, '/speckit-prd'), [ctx.relative(path)], ctx.name


def check_requirements(ctx):
    path = ctx.init_dir / 'requirements.yml'
    return bool(ctx.requirements), [ctx.relative(path)], ctx.name


def check_contracts(ctx):
    paths = [ctx.init_dir / name for name in CONTRACT_FILES]
    existing = [path for path in paths if path.is_file()]
    filled = [ctx.filled(path, '/speckit-contracts') for path in existing]
    return bool(existing) and all(filled), [ctx.relative(path) for path in existing or paths], ctx.name


def check_l4_file(ctx, file_name: str, command: str):
    """Done if every linked spec has this file filled. The target is the first one that does not."""
    missing = [spec.name for spec in ctx.specs if not ctx.filled(spec / file_name, command)]
    artifacts = [ctx.relative(spec / file_name) for spec in ctx.specs]
    return bool(ctx.specs) and not missing, artifacts, missing[0] if missing else None


def check_specify(ctx):
    done, artifacts, target = check_l4_file(ctx, 'spec.md', '/speckit-specify')
    return done, artifacts or ['.specify/specs/<NNN>-<slug>/spec.md'], target or '"<feature description>"'


def check_plan(ctx):
    return check_l4_file(ctx, 'plan.md', '/speckit-plan')


def task_lines(path: Path) -> set:
    return {line for line in path.read_text(encoding='utf-8').splitlines() if line.startswith('- [ ] **T')}


def check_tasks(ctx):
    """The task list of the template has no placeholders: it is unfilled if it is unchanged."""
    done, artifacts, target = check_l4_file(ctx, 'tasks.md', '/speckit-tasks')
    template = ctx.root / TEMPLATE_TASKS
    if not template.is_file():
        return done, artifacts, target
    template_lines = task_lines(template)
    for spec in ctx.specs:
        path = spec / 'tasks.md'
        if path.is_file() and template_lines <= task_lines(path):
            ctx.diagnostics.append(diagnostic(
                'warning', 'UNFILLED_TASKS', f"{ctx.relative(path)} still has the task list of the template",
                'Fill it with /speckit-tasks',
            ))
            return False, artifacts, target or spec.name
    return done, artifacts, target


def check_implement(ctx):
    done = bool(ctx.active_requirements) and all(
        req.get('status') in TERMINAL_STATUSES for req in ctx.active_requirements
    )
    target = ctx.specs[0].name if ctx.specs else ctx.name
    return done, [ctx.relative(ctx.init_dir / 'requirements.yml')], target


def check_trace(ctx):
    missing = [spec.name for spec in ctx.specs if not trace_rows(spec / 'trace.md')]
    artifacts = [ctx.relative(spec / 'trace.md') for spec in ctx.specs]
    return bool(ctx.specs) and not missing, artifacts, missing[0] if missing else None


def check_rtm(ctx):
    path = ctx.init_dir / 'trace.md'
    ids = {req['id'] for req in ctx.active_requirements}
    return bool(ids) and ids <= trace_rows(path), [ctx.relative(path)], ctx.name


def check_graduate(ctx):
    return bool(ctx.metadata.get('graduated')), [f"products/{ctx.metadata.get('product')}/requirements-registry.yml"], ctx.name


def check_rollout(ctx):
    path = ctx.init_dir / 'delivery' / 'rollout.md'
    return ctx.filled(path, '/speckit-release-rollout'), [ctx.relative(path)], ctx.name


# (id, command, check, applies to the Minimal profile)
STEPS = [
    ('prd', '/speckit-prd', check_prd, True),
    ('requirements', '/speckit-requirements', check_requirements, True),
    ('contracts', '/speckit-contracts', check_contracts, False),
    ('specify', '/speckit-specify', check_specify, True),
    ('plan', '/speckit-plan', check_plan, True),
    ('tasks', '/speckit-tasks', check_tasks, True),
    ('implement', '/speckit-implement', check_implement, True),
    ('trace', '/speckit-trace', check_trace, True),
    ('rtm', '/speckit-rtm', check_rtm, True),
    ('graduate', '/speckit-graduate', check_graduate, True),
    ('release-rollout', '/speckit-release-rollout', check_rollout, False),
]


def compute_steps(ctx: Context) -> list:
    minimal = ctx.metadata.get('profile', 'minimal') == 'minimal'
    implemented = check_implement(ctx)[0]
    steps = []
    open_ids = []
    for step_id, command, check, on_minimal in STEPS:
        if minimal and not on_minimal:
            continue
        step = {'id': step_id, 'command': command}
        if step_id in L4_STEPS and not ctx.specs and implemented:
            step.update(state='skipped', artifacts=[], reason='No L4 spec names this initiative')
            steps.append(step)
            continue
        done, artifacts, target = check(ctx)
        step['artifacts'] = artifacts
        if done:
            step['state'] = 'done'
        elif open_ids:
            step.update(state='blocked', blocked_by=list(open_ids))
        else:
            step.update(state='ready', target=target)
        if not done:
            open_ids.append(step_id)
        steps.append(step)
    return steps


def next_step(steps: list, profile: str) -> dict:
    step = next((item for item in steps if item['state'] == 'ready'), None)
    if not step:
        return None
    result = {'id': step['id'], 'command': f"{step['command']} {step.get('target') or ''}".strip()}
    if step['id'] == 'graduate' and profile != 'minimal':
        result['also_consider'] = ['/speckit-consilium']
    return result


def find_initiative(root: Path, name: str) -> Path:
    for parent in ('initiatives', 'archive'):
        path = root / parent / name
        if (path / 'requirements.yml').is_file():
            return path
    return None


def run(root: Path, name: str) -> dict:
    result = {
        'initiative': name, 'product': None, 'profile': None, 'initiative_status': None,
        'steps': [], 'next': None, 'diagnostics': [],
    }
    if not INITIATIVE_PATTERN.match(name):
        result['diagnostics'].append(diagnostic(
            'error', 'INVALID_INITIATIVE_ID', f"'{name}' does not match INIT-YYYY-NNN-slug",
            'Pass the initiative directory name',
        ))
        return result
    init_dir = find_initiative(root, name)
    if not init_dir:
        result['diagnostics'].append(diagnostic(
            'error', 'INITIATIVE_NOT_FOUND', f"No requirements.yml for {name} in initiatives/ or archive/",
            f"Run /speckit-start {name}",
        ))
        return result

    data = yaml.safe_load((init_dir / 'requirements.yml').read_text(encoding='utf-8')) or {}
    metadata = data.get('metadata') or {}
    requirements = [
        req for req in data.get('requirements') or []
        if req.get('id') and '{' not in req['id']
    ]
    result.update(
        product=metadata.get('product'),
        profile=metadata.get('profile'),
        initiative_status=metadata.get('initiative_status', 'active'),
    )
    if init_dir.parent.name == 'archive':
        result['initiative_status'] = 'archived'
        result['diagnostics'].append(diagnostic(
            'info', 'ARCHIVED', f"{name} is archived", f"Run tools/restore.sh {name} to continue the work",
        ))
        return result

    ctx = Context(root, init_dir, name, metadata, requirements)
    result['steps'] = compute_steps(ctx)
    result['next'] = next_step(result['steps'], metadata.get('profile', 'minimal'))
    result['diagnostics'] = ctx.diagnostics
    return result


def print_report(result: dict) -> None:
    print(f"{result['initiative']}  product: {result['product']}  profile: {result['profile']}  status: {result['initiative_status']}")
    for step in result['steps']:
        detail = ''
        if step.get('blocked_by'):
            detail = f"  (after {step['blocked_by'][0]})"
        elif step.get('reason'):
            detail = f"  ({step['reason']})"
        print(f"  {step['state']:<8} {step['id']}{detail}")
    for item in result['diagnostics']:
        print(f"  [{item['severity'].upper()}] {item['code']}: {item['message']}")
        print(f"    Fix: {item['fix']}")
    if result['next']:
        print(f"\nNext: {result['next']['command']}")
        for command in result['next'].get('also_consider', []):
            print(f"Also consider first: {command} {result['initiative']}")
    elif result['steps']:
        print('\nAll steps are done.')


def main():
    parser = argparse.ArgumentParser(description='Compute the state of an initiative from its files')
    parser.add_argument('initiative', help='INIT-YYYY-NNN-slug')
    parser.add_argument('--root', default='.', help='Repository root')
    parser.add_argument('--json', action='store_true', help='Print one JSON document to stdout')
    args = parser.parse_args()

    result = run(Path(args.root), args.initiative)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_report(result)
    sys.exit(1 if any(item['severity'] == 'error' for item in result['diagnostics']) else 0)


if __name__ == '__main__':
    main()
