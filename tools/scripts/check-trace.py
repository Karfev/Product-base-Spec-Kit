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
            trace.get('slo') or
            trace.get('architecture_views')
        )
        result[req_id] = has_evidence
    return result


def is_archived_spec(spec_dir: Path, root: Path) -> bool:
    """Check if a spec's parent initiative is archived."""
    spec_md = spec_dir / 'spec.md'
    if not spec_md.exists():
        return False
    try:
        text = spec_md.read_text()
        m = re.search(r'\*\*Initiative:\*\*\s*(\S+)', text)
        if m:
            init_id = m.group(1).strip()
            req_yml = root / 'initiatives' / init_id / 'requirements.yml'
            if req_yml.exists():
                with open(req_yml) as f:
                    data = yaml.safe_load(f)
                return data.get('metadata', {}).get('initiative_status') == 'archived'
    except Exception:
        pass
    return False


def parse_trace_md(path: Path) -> list:
    """Parse trace.md table. Returns list of REQ-IDs found."""
    pattern = re.compile(r'\|\s*`?(REQ-[A-Z0-9]{2,16}-[0-9]{3})`?\s*\|')
    req_ids = []
    for line in path.read_text().splitlines():
        m = pattern.search(line)
        if m:
            req_id = m.group(1)
            if '{' in req_id or '}' in req_id:
                continue
            req_ids.append(req_id)
    return req_ids


def main():
    root = Path('.')
    if '--root' in sys.argv:
        idx = sys.argv.index('--root')
        root = Path(sys.argv[idx + 1])

    errors = []
    warnings = []
    total_l4_req_refs = 0

    # Build L3 registry: {req_id: has_evidence}
    all_req_ids = {}
    for req_file in root.glob('initiatives/*/requirements.yml'):
        if is_template(req_file.parent):
            continue
        # Skip archived initiatives (INIT-2026-006)
        try:
            with open(req_file) as _f:
                _meta = yaml.safe_load(_f)
            if _meta.get('metadata', {}).get('initiative_status') == 'archived':
                continue
        except Exception:
            pass
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

    # Collect REQ-IDs from L3 initiative trace.md files
    all_l3_req_ids = set()
    total_l3_req_refs = 0
    for trace_file in root.glob('initiatives/*/trace.md'):
        if is_template(trace_file.parent):
            continue
        # Skip archived initiatives
        req_yml = trace_file.parent / 'requirements.yml'
        if req_yml.exists():
            try:
                with open(req_yml) as _f:
                    _meta = yaml.safe_load(_f)
                if _meta.get('metadata', {}).get('initiative_status') == 'archived':
                    continue
            except Exception:
                pass
        try:
            l3_ids = parse_trace_md(trace_file)
            total_l3_req_refs += len(l3_ids)
            all_l3_req_ids.update(l3_ids)
            for req_id in l3_ids:
                if req_id not in all_req_ids:
                    errors.append(
                        f"[ERROR] {trace_file}: REQ-ID '{req_id}' not found "
                        f"in any initiatives/*/requirements.yml"
                    )
        except Exception as e:
            errors.append(f"[ERROR] Cannot parse {trace_file}: {e}")

    # Check L3→L4 reverse: every REQ-ID from requirements.yml should appear in some trace.md (L3 or L4)
    l4_trace_files = [
        f for f in root.glob('.specify/specs/*/trace.md')
        if not is_template(f.parent) and not is_archived_spec(f.parent, root)
    ]
    all_l4_req_ids = set()
    for trace_file in l4_trace_files:
        try:
            all_l4_req_ids.update(parse_trace_md(trace_file))
        except Exception:
            pass

    all_traced_req_ids = all_l3_req_ids | all_l4_req_ids
    for req_id in all_req_ids:
        if req_id not in all_traced_req_ids:
            warnings.append(
                f"[WARN] REQ-ID '{req_id}' from requirements.yml has no "
                f"entry in any trace.md (L3 or L4)"
            )

    # Check L4 trace.md references exist in L3
    for trace_file in root.glob('.specify/specs/*/trace.md'):
        if is_template(trace_file.parent):
            continue
        if is_archived_spec(trace_file.parent, root):
            continue
        try:
            l4_req_ids = parse_trace_md(trace_file)
            total_l4_req_refs += len(l4_req_ids)
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

    trace_summary = (
        f"{total_l3_req_refs} REQ-ID(s) in L3, "
        f"{total_l4_req_refs} REQ-ID(s) in L4"
    )
    if errors:
        print(
            f"\n❌ check-trace: {len(errors)} error(s), {len(warnings)} warning(s), "
            f"{trace_summary}"
        )
        sys.exit(1)
    elif warnings:
        print(
            f"\n⚠️  check-trace: 0 errors, {len(warnings)} warning(s), "
            f"{trace_summary}"
        )
    else:
        print(
            "✅ check-trace: all REQ-ID references are consistent "
            f"({trace_summary})"
        )


if __name__ == '__main__':
    main()
