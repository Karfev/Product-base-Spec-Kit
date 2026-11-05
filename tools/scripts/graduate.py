#!/usr/bin/env python3
"""
Graduate an initiative into the product layer (L2): requirements, ADRs, knowledge log.

The registry products/<product>/requirements-registry.yml describes how the product
works now. requirements.yml of an initiative is a proposed change to it.

Merge rules. A requirement whose history already names this initiative is a no-op,
so running the script again is safe.

  delta      status in initiative   condition            result
  added      implemented, verified  ID is free           new entry, rev 1
  added      implemented, verified  ID exists            conflict
  modified   implemented, verified  base_rev == rev      rev + 1, text replaced
  modified   implemented, verified  otherwise            conflict
  removed    deprecated             base_rev == rev      rev + 1, status deprecated
  removed    deprecated             otherwise            conflict
  any        any other              -                    stays in the initiative

A missing delta means added. A deprecated entry stays in the registry and its ID is
not reused. All changes are planned in memory and written only if there are no
conflicts. Contracts are merged by /speckit-graduate, not here.

Usage:
  python tools/scripts/graduate.py <INIT> [--root <path>] [--dry-run] [--only ID,...]
                                   [--skip-adr ADR,...] [--force] [--json]

  --dry-run   report the plan, write nothing
  --only      merge only these REQ-IDs; the initiative is not marked as graduated
              while other requirements are still eligible
  --skip-adr  do not copy these ADRs (file names without .md)
  --force     run on an initiative that already has graduated: true
  --json      print one JSON document to stdout

Exit codes:
  0 — applied, or nothing to do
  1 — conflicts or invalid input, nothing written
"""
import argparse
import json
import os
import re
import sys
from datetime import date
from itertools import takewhile
from pathlib import Path
from tempfile import NamedTemporaryFile

import yaml

ELIGIBLE_STATUSES = {'implemented', 'verified'}
INITIATIVE_PATTERN = re.compile(r'^INIT-[0-9]{4}-[0-9]{3}-[a-z0-9-]+$')
ADR_FILE_PATTERN = re.compile(r'^([A-Z][A-Z0-9]*)-([0-9]{4})-.+\.md$')
ADR_NON_DECISIONS = {'README.md', 'ADR-template.md'}
REGISTRY_SCHEMA_VERSION = 2
REGISTRY_HEADER = (
    '# Product requirements registry: how the product works now.\n'
    '# Auto-maintained by tools/scripts/graduate.py. Do not edit manually.\n'
)
LOG_HEADER = '# Knowledge Log: {product}\n\nGraduation history — newest first. Auto-maintained by `/speckit-graduate`.\n'


class RegistrySchemaError(Exception):
    """The registry was not written by this version of the tool."""


class RegistryDumper(yaml.SafeDumper):
    """Indent list items under their key, as yamllint expects."""

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def diagnostic(code: str, message: str, fix: str, req_id: str = None) -> dict:
    item = {'severity': 'error', 'code': code, 'message': message, 'fix': fix}
    if req_id:
        item['id'] = req_id
    return item


def load_initiative(path: Path) -> tuple:
    """Parse requirements.yml. Returns (metadata, requirements without placeholders)."""
    data = yaml.safe_load(path.read_text()) or {}
    requirements = [
        req for req in data.get('requirements') or []
        if req.get('id') and '{' not in req['id']
    ]
    return data.get('metadata') or {}, requirements


def load_registry(path: Path) -> tuple:
    """Returns (header comment, registry data). A missing file gives an empty registry."""
    if not path.exists():
        return REGISTRY_HEADER, None
    text = path.read_text()
    data = yaml.safe_load(text) or {}
    if (data.get('metadata') or {}).get('schema_version') != REGISTRY_SCHEMA_VERSION:
        raise RegistrySchemaError(
            f"{path} has no metadata.schema_version: {REGISTRY_SCHEMA_VERSION}"
        )
    header = ''.join(takewhile(lambda line: line.startswith('#') or not line.strip(), text.splitlines(keepends=True)))
    return header, data


def dump_registry(header: str, data: dict) -> str:
    return header + yaml.dump(data, Dumper=RegistryDumper, allow_unicode=True, sort_keys=False, width=100)


def classify(req: dict, entry: dict, initiative: str, ignore_status: bool = False) -> tuple:
    """Apply the merge rules. Returns (noop | pending | apply | conflict, diagnostic or None)."""
    req_id = req['id']
    delta = req.get('delta', 'added')
    if entry and any(item.get('initiative') == initiative for item in entry.get('history') or []):
        return 'noop', None
    if not ignore_status:
        required = {'deprecated'} if delta == 'removed' else ELIGIBLE_STATUSES
        if req.get('status') not in required:
            return 'pending', None

    if delta == 'added':
        if entry:
            return 'conflict', diagnostic(
                'ID_EXISTS', f"{req_id} already exists in the registry at rev {entry.get('rev')}",
                f"Set delta: modified and base_rev: {entry.get('rev')} to change it, or choose a new REQ-ID",
                req_id,
            )
        return 'apply', None
    if delta not in ('modified', 'removed'):
        return 'conflict', diagnostic(
            'INVALID_DELTA', f"{req_id} has delta '{delta}'", 'Use added, modified or removed', req_id,
        )
    if not entry:
        return 'conflict', diagnostic(
            'NO_REGISTRY_ENTRY', f"{req_id} has delta: {delta}, but the registry has no such entry",
            'Remove delta and base_rev to add it as a new requirement, or fix the REQ-ID', req_id,
        )
    if entry.get('status') == 'deprecated':
        return 'conflict', diagnostic(
            'ENTRY_DEPRECATED', f"{req_id} is deprecated in the registry and cannot be changed",
            'Choose a new REQ-ID: a deprecated ID is not reused', req_id,
        )
    if req.get('base_rev') != entry.get('rev'):
        return 'conflict', diagnostic(
            'STALE_BASE_REV',
            f"{req_id} is based on rev {req.get('base_rev')}, the registry is at rev {entry.get('rev')} "
            f"(last changed by {entry.get('source_initiative')})",
            f"Review the current text in the registry, update the requirement, set base_rev: {entry.get('rev')}",
            req_id,
        )
    if delta == 'removed' and not req.get('removal_reason'):
        return 'conflict', diagnostic(
            'MISSING_REMOVAL_REASON', f"{req_id} has delta: removed without removal_reason",
            'Add removal_reason', req_id,
        )
    return 'apply', None


def apply_requirement(req: dict, entry: dict, initiative: str, today: str) -> dict:
    """Return the registry entry after the change."""
    delta = req.get('delta', 'added')
    rev = entry['rev'] + 1 if entry else 1
    history = (entry.get('history') if entry else None) or []
    if delta == 'removed':
        result = dict(entry)
        result.update(status='deprecated', removal_reason=req['removal_reason'])
    else:
        result = {
            'id': req['id'],
            'title': req['title'],
            'type': req['type'],
            'priority': req['priority'],
            'status': req['status'],
            'description': req['description'].strip(),
        }
        for field in ('acceptance_criteria', 'metrics'):
            if req.get(field):
                result[field] = req[field]
    result.update(
        rev=rev,
        source_initiative=initiative,
        graduated_date=today,
        history=history + [{'rev': rev, 'initiative': initiative, 'date': today, 'change': delta}],
    )
    return result


def adr_directories(root: Path, product_dir: Path) -> list:
    return [product_dir / 'decisions', root / 'decisions']


def adr_prefix(product: str, product_dir: Path) -> str:
    for path in sorted((product_dir / 'decisions').glob('*.md')):
        match = ADR_FILE_PATTERN.match(path.name)
        if match:
            return match.group(1)
    return re.sub(r'[^A-Z0-9]', '', product.upper())[:4]


def next_adr_number(prefix: str, root: Path, product_dir: Path) -> int:
    numbers = [0]
    for directory in adr_directories(root, product_dir):
        for path in directory.glob('*.md'):
            match = ADR_FILE_PATTERN.match(path.name)
            if match and match.group(1) == prefix:
                numbers.append(int(match.group(2)))
    return max(numbers) + 1


def graduated_adr_sources(product_dir: Path) -> set:
    sources = set()
    for path in (product_dir / 'decisions').glob('*.md'):
        match = re.search(r'^original_id:\s*["\']?([^"\'\n]+)', path.read_text(), re.M)
        if match:
            sources.add(match.group(1).strip())
    return sources


def split_frontmatter(text: str) -> tuple:
    if text.startswith('---\n'):
        end = text.find('\n---\n', 3)
        if end != -1:
            return text[4:end + 1], text[end + 5:]
    return '', text


def adr_title(body: str) -> str:
    match = re.search(r'^# (.*)$', body, re.M)
    title = match.group(1) if match else ''
    return re.sub(r'^[^\s:]*ADR-[0-9]+[^\s:]*:\s*', '', title).strip()


def graduate_adr(text: str, adr_id: str, initiative: str, original_id: str, today: str) -> str:
    """Add graduation fields to the frontmatter and put the product ID into the heading."""
    frontmatter, body = split_frontmatter(text)
    frontmatter += (
        f'graduated_from: "{initiative}"\n'
        f'original_id: "{original_id}"\n'
        f'graduated_date: "{today}"\n'
    )
    title = adr_title(body)
    heading = f'# {adr_id}: {title}'.rstrip()
    body, replaced = re.subn(r'^# .*$', lambda _: heading, body, count=1, flags=re.M)
    if not replaced:
        body = f'{heading}\n\n{body}'
    return f'---\n{frontmatter}---\n\n{body.lstrip()}'


def plan_adrs(root: Path, init_dir: Path, product: str, product_dir: Path, initiative: str,
              skip: list, today: str) -> tuple:
    """Returns (report items, {target path: text})."""
    done = graduated_adr_sources(product_dir)
    prefix = adr_prefix(product, product_dir)
    number = next_adr_number(prefix, root, product_dir)
    items, files = [], {}
    for path in sorted((init_dir / 'decisions').glob('*.md')):
        if path.name in ADR_NON_DECISIONS or '{' in path.name or path.stem in done or path.stem in skip:
            continue
        match = re.search(r'-ADR-[0-9]+-(.+)$', path.stem)
        slug = match.group(1) if match else path.stem
        adr_id = f'{prefix}-{number:04d}'
        text = path.read_text()
        files[product_dir / 'decisions' / f'{adr_id}-{slug}.md'] = graduate_adr(
            text, adr_id, initiative, path.stem, today,
        )
        items.append({
            'source': path.stem,
            'target': f'{adr_id}-{slug}',
            'title': adr_title(split_frontmatter(text)[1]),
        })
        number += 1
    return items, files


def extract_outcome(init_dir: Path) -> str:
    path = init_dir / 'prd.md'
    if not path.exists():
        return '—'
    match = re.search(r'\*\*Цель \(Outcome\):\*\*\s*(.+)', path.read_text())
    if not match or '{' in match.group(1):
        return '—'
    return match.group(1).strip()


def knowledge_log_section(initiative: str, today: str, outcome: str, merged: list, adrs: list) -> str:
    lines = [f'## {today} — {initiative}', '', f'**Outcome:** {outcome}', '']
    if merged:
        lines += [
            '### Requirements graduated', '',
            '| REQ-ID | Title | Final Status | Type | Change |',
            '|---|---|---|---|---|',
        ]
        lines += [
            f"| {item['id']} | {item['title']} | {item['status']} | {item['type']} | {item['delta']}, rev {item['rev']} |"
            for item in merged
        ]
        lines.append('')
    if adrs:
        lines += ['### ADRs graduated', '', '| Source | Product ADR | Title |', '|---|---|---|']
        lines += [f"| {item['source']} | {item['target']} | {item['title']} |" for item in adrs]
        lines.append('')
    lines += ['### Key learnings', '', '{placeholder — add key insights from this initiative}', '']
    return '\n'.join(lines)


def prepend_to_log(log_text: str, product: str, section: str) -> str:
    """Put the section before the newest one, keeping the header of the log."""
    log_text = log_text or LOG_HEADER.format(product=product)
    head, separator, rest = log_text.partition('\n---\n')
    if not separator:
        return f'{head.rstrip()}\n\n---\n\n{section}'
    return f'{head}\n---\n\n{section}\n---\n{rest}'


def mark_graduated(text: str, today: str) -> str:
    """Edit the metadata block line by line, so comments and formatting of the file survive."""
    lines = text.splitlines(keepends=True)
    start = next((i for i, line in enumerate(lines) if line.rstrip() == 'metadata:'), None)
    if start is None:
        return text
    end = start + 1
    while end < len(lines) and (lines[end].startswith((' ', '\t', '#')) or not lines[end].strip()):
        end += 1
    block = range(start + 1, end)
    updated = next((i for i in block if lines[i].lstrip().startswith('last_updated:')), None)
    graduated = next((i for i in block if lines[i].lstrip().startswith('graduated:')), None)
    if updated is not None:
        lines[updated] = re.sub(
            r'(last_updated:\s*)(["\']?)[^"\'\s]*\2',
            lambda m: f'{m.group(1)}{m.group(2)}{today}{m.group(2)}',
            lines[updated],
        )
    if graduated is not None:
        lines[graduated] = re.sub(r'(graduated:\s*)\S+', r'\1true', lines[graduated])
    elif updated is not None:
        indent = lines[updated][:len(lines[updated]) - len(lines[updated].lstrip())]
        lines.insert(updated + 1, f'{indent}graduated: true\n')
    return ''.join(lines)


def write_files(files: dict) -> None:
    for path, text in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        mode = path.stat().st_mode if path.exists() else 0o644
        with NamedTemporaryFile('w', dir=path.parent, delete=False, encoding='utf-8') as temporary:
            temporary.write(text)
        os.chmod(temporary.name, mode)
        os.replace(temporary.name, path)


def run(root: Path, name: str, today: str = None, dry_run: bool = False, force: bool = False,
        only: list = None, skip_adrs: list = None) -> dict:
    """Plan the graduation and apply it unless there are conflicts or dry_run is set."""
    today = today or date.today().isoformat()
    result = {
        'initiative': name, 'product': None, 'dry_run': dry_run, 'already_graduated': False,
        'merged': [], 'noop': [], 'pending': [], 'conflicts': [], 'adrs': [],
        'knowledge_log': False, 'graduated': False,
    }
    conflicts = result['conflicts']

    if not INITIATIVE_PATTERN.match(name):
        conflicts.append(diagnostic(
            'INVALID_INITIATIVE_ID', f"'{name}' does not match INIT-YYYY-NNN-slug", 'Pass the initiative directory name',
        ))
        return result
    init_dir = root / 'initiatives' / name
    req_path = init_dir / 'requirements.yml'
    if not req_path.exists():
        conflicts.append(diagnostic(
            'INITIATIVE_NOT_FOUND', f"{req_path} not found", 'Restore the initiative first if it is archived',
        ))
        return result

    metadata, requirements = load_initiative(req_path)
    product = metadata.get('product')
    result['product'] = product
    if metadata.get('graduated') and not force:
        result['already_graduated'] = True
        return result
    product_dir = root / 'products' / str(product)
    if not product_dir.is_dir():
        conflicts.append(diagnostic(
            'PRODUCT_NOT_FOUND', f"{product_dir} not found", f"Run /speckit-product-init {product}",
        ))
        return result

    registry_path = product_dir / 'requirements-registry.yml'
    try:
        header, registry = load_registry(registry_path)
    except RegistrySchemaError as error:
        conflicts.append(diagnostic(
            'REGISTRY_SCHEMA', str(error), 'Migrate the registry, see decisions/PLAT-0005-requirements-delta-model.md',
        ))
        return result
    if registry is None:
        registry = {
            'metadata': {
                'schema_version': REGISTRY_SCHEMA_VERSION,
                'product': product,
                'owner': metadata.get('owner'),
                'last_updated': today,
            },
            'entries': [],
        }
    entries = {entry['id']: entry for entry in registry['entries']}

    ids = [req['id'] for req in requirements]
    selected = set(only) if only else set(ids)
    for unknown in sorted(selected - set(ids)):
        conflicts.append(diagnostic(
            'UNKNOWN_ID', f"{unknown} is not in {req_path}", 'Fix the value of --only', unknown,
        ))
    left_behind = False
    for req in requirements:
        req_id = req['id']
        if ids.count(req_id) > 1:
            if not any(item.get('id') == req_id for item in conflicts):
                conflicts.append(diagnostic(
                    'DUPLICATE_ID', f"{req_id} appears more than once in {req_path}", 'Keep one definition', req_id,
                ))
            continue
        action, problem = classify(req, entries.get(req_id), name)
        if req_id not in selected:
            left_behind = left_behind or action in ('apply', 'conflict')
        elif action == 'conflict':
            conflicts.append(problem)
        elif action == 'noop':
            result['noop'].append(req_id)
        elif action == 'pending':
            result['pending'].append(req_id)
        else:
            entries[req_id] = apply_requirement(req, entries.get(req_id), name, today)
            result['merged'].append({
                'id': req_id,
                'title': entries[req_id]['title'],
                'type': entries[req_id]['type'],
                'status': entries[req_id]['status'],
                'delta': req.get('delta', 'added'),
                'rev': entries[req_id]['rev'],
            })

    result['adrs'], files = plan_adrs(root, init_dir, str(product), product_dir, name, skip_adrs or [], today)
    if conflicts:
        result['merged'], result['adrs'] = [], []
        return result

    changed = bool(result['merged'] or result['adrs'])
    if result['merged']:
        registry['entries'] = list(entries.values())
        registry['metadata']['last_updated'] = today
        files[registry_path] = dump_registry(header, registry)
    if changed:
        log_path = product_dir / 'knowledge-log.md'
        section = knowledge_log_section(name, today, extract_outcome(init_dir), result['merged'], result['adrs'])
        files[log_path] = prepend_to_log(log_path.read_text() if log_path.exists() else '', str(product), section)
        result['knowledge_log'] = True

    done_something = changed or result['noop']
    if done_something and not left_behind and not metadata.get('graduated'):
        text = mark_graduated(req_path.read_text(), today)
        if not (yaml.safe_load(text).get('metadata') or {}).get('graduated'):
            conflicts.append(diagnostic(
                'METADATA_EDIT', f"Cannot set metadata.graduated in {req_path}",
                'Write metadata as a block mapping with one field per line',
            ))
            result['merged'], result['adrs'], result['knowledge_log'] = [], [], False
            return result
        files[req_path] = text
        result['graduated'] = not dry_run
    elif metadata.get('graduated'):
        result['graduated'] = True

    if not dry_run:
        write_files(files)
    return result


def print_report(result: dict) -> None:
    label = 'Plan' if result['dry_run'] else 'Graduation'
    print(f"{label} for {result['initiative']} -> products/{result['product']}/")
    if result['already_graduated']:
        print('  Already graduated, nothing changed. Use --force to merge requirements that became eligible later.')
        return
    for item in result['merged']:
        print(f"  merge  {item['id']}  {item['delta']}, rev {item['rev']}, {item['status']}")
    for item in result['adrs']:
        print(f"  adr    {item['source']} -> {item['target']}")
    if result['noop']:
        print(f"  already merged: {', '.join(result['noop'])}")
    if result['pending']:
        print(f"  stay in the initiative (status not eligible): {', '.join(result['pending'])}")
    for item in result['conflicts']:
        print(f"  [CONFLICT] {item['code']}: {item['message']}")
        print(f"    Fix: {item['fix']}")
    if result['conflicts']:
        print('\nNothing written.')
    elif result['dry_run']:
        print('\nDry run, nothing written.')
    elif not (result['merged'] or result['adrs']):
        print('\nNothing to graduate.')


def parse_list(value: str) -> list:
    return [item.strip() for item in value.split(',') if item.strip()]


def main():
    parser = argparse.ArgumentParser(description='Graduate an initiative into the product layer')
    parser.add_argument('initiative', help='INIT-YYYY-NNN-slug')
    parser.add_argument('--root', default='.', help='Repository root')
    parser.add_argument('--dry-run', action='store_true', help='Report the plan, write nothing')
    parser.add_argument('--only', type=parse_list, help='Merge only these REQ-IDs (comma separated)')
    parser.add_argument('--skip-adr', type=parse_list, help='Do not copy these ADRs (comma separated, no .md)')
    parser.add_argument('--force', action='store_true', help='Run on an initiative that is already graduated')
    parser.add_argument('--json', action='store_true', help='Print one JSON document to stdout')
    args = parser.parse_args()

    result = run(
        Path(args.root), args.initiative, dry_run=args.dry_run, force=args.force,
        only=args.only, skip_adrs=args.skip_adr,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_report(result)
    sys.exit(1 if result['conflicts'] else 0)


if __name__ == '__main__':
    main()
