#!/usr/bin/env python3
"""
Collect GSD execution evidence from SUMMARY.md files into an RTM report.

Scans .planning/phases/SPEC-*/*-SUMMARY.md for completed requirements,
cross-references with initiatives/*/requirements.yml, and outputs an
evidence/rtm-{date}.md traceability report.

Usage:
  python tools/scripts/collect-evidence.py [--root <path>]

Exit codes:
  0 — always (graceful if no .planning/ exists)
"""
import sys
import re
import yaml
from pathlib import Path
from datetime import date


REQ_PATTERN = re.compile(r'REQ-[A-Z0-9]{2,16}-[0-9]{3}')


def is_template(path: Path) -> bool:
    """Skip template placeholder directories containing {braces}."""
    return '{' in str(path)


def parse_requirements_yml(path: Path) -> dict:
    """Parse requirements.yml. Returns {req_id: {title, status, initiative}}."""
    with open(path) as f:
        data = yaml.safe_load(f)
    result = {}
    initiative = data.get('metadata', {}).get('initiative', str(path.parent.name))
    for req in data.get('requirements', []):
        req_id = req.get('id', '')
        if not req_id or '{' in req_id:
            continue
        result[req_id] = {
            'title': req.get('title', ''),
            'status': req.get('status', 'unknown'),
            'initiative': initiative,
        }
    return result


def parse_summary_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from SUMMARY.md if present."""
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            try:
                return yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                pass
    return {}


def detect_status(text: str, frontmatter: dict) -> str:
    """Detect plan execution status. Prefers structured frontmatter over heuristics.

    Returns: PASS, PARTIAL, FAIL, or UNKNOWN.
    """
    # Prefer structured status from frontmatter
    fm_status = str(frontmatter.get('status', '')).upper()
    if fm_status in ('PASS', 'PASSED', 'COMPLETE', 'COMPLETED', 'SUCCESS'):
        return 'PASS'
    if fm_status in ('FAIL', 'FAILED', 'FAILURE'):
        return 'FAIL'
    if fm_status in ('PARTIAL', 'INCOMPLETE', 'BLOCKED'):
        return 'PARTIAL'

    # Fallback: scan only status/verification sections, not full text
    # Split into sections and look for verification/status headings
    status_text = ''
    in_status_section = False
    for line in text.splitlines():
        lower_line = line.lower().strip()
        if lower_line.startswith('#') and any(
            kw in lower_line for kw in ('verification', 'status', 'result', 'summary')
        ):
            in_status_section = True
            continue
        elif lower_line.startswith('#'):
            in_status_section = False
        if in_status_section:
            status_text += line + '\n'

    # If no status section found, use last 20 lines as status context
    if not status_text:
        status_text = '\n'.join(text.splitlines()[-20:])

    lower = status_text.lower()
    if 'failed' in lower or 'failure' in lower:
        return 'FAIL'
    if 'blocked' in lower or 'incomplete' in lower:
        return 'PARTIAL'
    if 'all tasks completed' in lower or 'passed' in lower:
        return 'PASS'

    return 'UNKNOWN'


def parse_summary_md(path: Path) -> dict:
    """Parse a GSD SUMMARY.md file. Returns {req_ids: [...], status: str, plan: str}."""
    text = path.read_text()
    req_ids = list(set(REQ_PATTERN.findall(text)))

    # Determine plan ID from filename (e.g., 01-03-SUMMARY.md -> 01-03)
    plan_id = path.stem.replace('-SUMMARY', '')

    frontmatter = parse_summary_frontmatter(text)
    status = detect_status(text, frontmatter)

    return {
        'req_ids': req_ids,
        'status': status,
        'plan': plan_id,
        'spec': path.parent.name,
    }


def main():
    root = Path('.')
    if '--root' in sys.argv:
        idx = sys.argv.index('--root')
        if idx + 1 >= len(sys.argv):
            print("Error: --root requires a path argument", file=sys.stderr)
            sys.exit(1)
        root = Path(sys.argv[idx + 1])

    planning_dir = root / '.planning' / 'phases'
    evidence_dir = root / 'evidence'

    # Graceful exit if no .planning/ exists
    if not planning_dir.exists():
        print("No .planning/phases/ directory found — nothing to collect")
        sys.exit(0)

    # Collect all SUMMARY.md files
    summaries = sorted(planning_dir.glob('SPEC-*/*-SUMMARY.md'))
    if not summaries:
        print("No SUMMARY.md files found in .planning/phases/SPEC-*/ — nothing to collect")
        sys.exit(0)

    # Build L3 registry
    all_reqs = {}
    for req_file in root.glob('initiatives/*/requirements.yml'):
        if is_template(req_file.parent):
            continue
        try:
            reqs = parse_requirements_yml(req_file)
            all_reqs.update(reqs)
        except Exception as e:
            print(f"[WARN] Cannot parse {req_file}: {e}", file=sys.stderr)

    # Parse all summaries (sorted by filename = wave execution order)
    # "Last wins" strategy: later plans override earlier ones for same REQ-ID,
    # since plans execute in wave order and later results are more authoritative.
    req_coverage = {}  # {req_id: {plan, status, spec}}
    for summary_path in summaries:
        try:
            summary = parse_summary_md(summary_path)
            for req_id in summary['req_ids']:
                req_coverage[req_id] = {
                    'plan': summary['plan'],
                    'status': summary['status'],
                    'spec': summary['spec'],
                }
        except Exception as e:
            print(f"[WARN] Cannot parse {summary_path}: {e}", file=sys.stderr)

    # Generate RTM report
    today = date.today().isoformat()
    evidence_dir.mkdir(parents=True, exist_ok=True)
    output_path = evidence_dir / f'rtm-{today}.md'

    lines = [
        f'# Requirements Traceability Matrix — {today}',
        '',
        f'Generated by `collect-evidence.py` from `.planning/phases/` SUMMARY files.',
        '',
        '## Coverage',
        '',
        '| REQ-ID | Title | Initiative | Plan | Spec | Status |',
        '|--------|-------|------------|------|------|--------|',
    ]

    total = len(all_reqs)
    passed = 0
    failed = 0
    partial = 0
    missing = 0

    for req_id in sorted(all_reqs.keys()):
        req_info = all_reqs[req_id]
        coverage = req_coverage.get(req_id)

        if coverage:
            status = coverage['status']
            plan = coverage['plan']
            spec = coverage['spec']
            if status == 'PASS':
                passed += 1
            elif status == 'FAIL':
                failed += 1
            else:
                partial += 1
        else:
            status = 'NOT COVERED'
            plan = '—'
            spec = '—'
            missing += 1

        lines.append(
            f"| {req_id} | {req_info['title']} | {req_info['initiative']} "
            f"| {plan} | {spec} | {status} |"
        )

    lines.extend([
        '',
        '## Summary',
        '',
        f'- **Total requirements:** {total}',
        f'- **Passed:** {passed}',
        f'- **Failed:** {failed}',
        f'- **Partial:** {partial}',
        f'- **Not covered:** {missing}',
        f'- **Coverage:** {(passed / total * 100) if total > 0 else 0:.0f}%',
        '',
        '## Sources',
        '',
    ])

    for summary_path in summaries:
        lines.append(f'- `{summary_path.relative_to(root)}`')

    lines.append('')

    output_path.write_text('\n'.join(lines))
    print(f"RTM report written to {output_path}")
    print(f"  {total} requirements: {passed} passed, {failed} failed, {partial} partial, {missing} not covered")


if __name__ == '__main__':
    main()
