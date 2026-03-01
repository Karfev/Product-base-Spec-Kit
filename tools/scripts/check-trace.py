#!/usr/bin/env python3
"""
Check REQ-ID consistency between L3 (requirements.yml) and L4 (trace.md).

Checks:
  1. Every REQ-ID referenced in L4 trace.md exists in some L3 requirements.yml
  2. Every REQ-ID in requirements.yml has at least one trace evidence entry
     (tests, contracts, or slo must be non-empty)

Usage:
  python tools/scripts/check-trace.py [--root <path>]

Exit codes:
  0 — all checks passed (warnings may be printed)
  1 — errors found (missing REQ-IDs)
"""
import sys
import re
import yaml
from pathlib import Path


def is_template(path: Path) -> bool:
    """Skip template placeholder directories containing {braces}."""
    return '{' in str(path)


def parse_requirements_yml(path: Path) -> dict:
    """Parse requirements.yml. Returns {req_id: has_trace_evidence}."""
    with open(path) as f:
        data = yaml.safe_load(f)
    result = {}
    for req in data.get('requirements', []):
        req_id = req.get('id', '')
        if not req_id or '{' in req_id:
            continue
        trace = req.get('trace', {}) or {}
        has_evidence = bool(
            trace.get('tests') or
            trace.get('contracts') or
            trace.get('slo')
        )
        result[req_id] = has_evidence
    return result


def parse_trace_md(path: Path) -> list:
    """Parse trace.md table. Returns list of REQ-IDs found."""
    pattern = re.compile(r'\|\s*(REQ-[A-Z0-9]{2,16}-[0-9]{3})\s*\|')
    req_ids = []
    for line in path.read_text().splitlines():
        m = pattern.search(line)
        if m:
            req_ids.append(m.group(1))
    return req_ids


def main():
    root = Path('.')
    if '--root' in sys.argv:
        idx = sys.argv.index('--root')
        root = Path(sys.argv[idx + 1])

    errors = []
    warnings = []

    # Build L3 registry: {req_id: has_evidence}
    all_req_ids = {}
    for req_file in root.glob('initiatives/*/requirements.yml'):
        if is_template(req_file.parent):
            continue
        try:
            reqs = parse_requirements_yml(req_file)
            for req_id, has_evidence in reqs.items():
                all_req_ids[req_id] = has_evidence
                if not has_evidence:
                    warnings.append(
                        f"[WARN] {req_file}: {req_id} has no trace evidence "
                        f"(tests/contracts/slo are empty)"
                    )
        except Exception as e:
            errors.append(f"[ERROR] Cannot parse {req_file}: {e}")

    # Check L4 trace.md references exist in L3
    for trace_file in root.glob('.specify/specs/*/trace.md'):
        if is_template(trace_file.parent):
            continue
        try:
            l4_req_ids = parse_trace_md(trace_file)
            for req_id in l4_req_ids:
                if req_id not in all_req_ids:
                    errors.append(
                        f"[ERROR] {trace_file}: REQ-ID '{req_id}' not found "
                        f"in any initiatives/*/requirements.yml"
                    )
        except Exception as e:
            errors.append(f"[ERROR] Cannot parse {trace_file}: {e}")

    for w in warnings:
        print(w)
    for e in errors:
        print(e)

    if errors:
        print(f"\n❌ check-trace: {len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(1)
    elif warnings:
        print(f"\n⚠️  check-trace: 0 errors, {len(warnings)} warning(s)")
    else:
        print("✅ check-trace: all REQ-ID references are consistent")


if __name__ == '__main__':
    main()
