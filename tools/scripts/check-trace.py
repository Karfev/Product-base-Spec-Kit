#!/usr/bin/env python3
"""
Check REQ-ID consistency and trace links between L3 (requirements.yml) and L4 (trace.md).

Checks:
  1. Every REQ-ID referenced in a trace.md exists in some L3 requirements.yml
  2. Every link in requirement.trace resolves (file, YAML fragment, SLO name, ADR, test tag)
  3. Every requirement has at least one trace evidence entry
  4. Every requirement appears in some trace.md (L3 or L4)

Severity (status of the requirement):
  implemented, verified — broken link and empty evidence are errors,
                          missing trace.md row is an error for Standard+
  other statuses        — warnings; links may describe work that is still planned
  deprecated            — evidence and trace.md rows are not required

examples/*/requirements.yml are checked for links and evidence only: their REQ-IDs
do not join the initiative registry.

External tests use the form ext:<repo>/<path>::REQ-ID. Only the format and REQ-ID are
checked. No check here proves that a test passes.

Usage:
  python tools/scripts/check-trace.py [--root <path>] [--strict]

  --strict  report broken links as errors for every status

Exit codes:
  0 — all checks passed (warnings may be printed)
  1 — errors found
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

TERMINAL_STATUSES = {'implemented', 'verified'}
EVIDENCE_FIELDS = ('tests', 'contracts', 'slo', 'architecture_views')
YAML_SUFFIXES = {'.yaml', '.yml', '.json'}
REQ_ID_PATTERN = re.compile(r'^REQ-[A-Z0-9]{2,16}-[0-9]{3}$')
EXTERNAL_TEST_PATTERN = re.compile(r'^ext:[^/\s]+/\S+$')


def is_template(path: Path) -> bool:
    """Skip template placeholder directories containing {braces}."""
    return '{' in str(path)


def load_requirements(path: Path) -> tuple:
    """Parse requirements.yml. Returns (metadata, requirements without placeholders)."""
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    requirements = [
        req for req in data.get('requirements') or []
        if req.get('id') and '{' not in req['id']
    ]
    return data.get('metadata') or {}, requirements


def has_evidence(req: dict) -> bool:
    trace = req.get('trace') or {}
    return any(trace.get(field) for field in EVIDENCE_FIELDS)


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


def find_file(ref_path: str, init_dir: Path, root: Path):
    """Resolve a reference relative to the initiative, then to the repository root."""
    for base in (init_dir, root):
        candidate = base / ref_path
        if candidate.is_file():
            return candidate
    return None


def load_documents(path: Path) -> list:
    return [doc for doc in yaml.safe_load_all(path.read_text()) if doc is not None]


def fragment_resolves(document, fragment: str) -> bool:
    """Walk a JSON Pointer, with or without the leading slash."""
    node = document
    for raw_segment in fragment.strip('/').split('/'):
        segment = raw_segment.replace('~1', '/').replace('~0', '~')
        if isinstance(node, dict):
            keys = {str(key): key for key in node}
            if segment not in keys:
                return False
            node = node[keys[segment]]
        elif isinstance(node, list) and segment.isdigit() and int(segment) < len(node):
            node = node[int(segment)]
        else:
            return False
    return True


def check_test_ref(ref: str, req_id: str, init_dir: Path, root: Path):
    ref_path, separator, tag = ref.partition('::')
    if separator and REQ_ID_PATTERN.match(tag) and tag != req_id:
        return f"test '{ref}' is tagged for {tag}, not {req_id}"
    if ref.startswith('ext:'):
        if not separator or not EXTERNAL_TEST_PATTERN.match(ref_path):
            return f"external test '{ref}' must look like ext:<repo>/<path>::{req_id}"
        return None
    path = find_file(ref_path, init_dir, root)
    if path is None:
        return f"test file not found: '{ref_path}'"
    if separator and tag not in path.read_text(errors='ignore'):
        return f"'{tag}' not found in test file '{ref_path}'"
    return None


def check_contract_ref(ref: str, init_dir: Path, root: Path):
    ref_path, separator, fragment = ref.partition('#')
    path = find_file(ref_path, init_dir, root)
    if path is None:
        return f"contract file not found: '{ref_path}'"
    if not separator or path.suffix not in YAML_SUFFIXES:
        return None
    try:
        documents = load_documents(path)
    except yaml.YAMLError:
        return f"cannot parse contract file: '{ref_path}'"
    if not any(fragment_resolves(document, fragment) for document in documents):
        return f"fragment '#{fragment}' not found in '{ref_path}'"
    return None


def check_file_ref(ref: str, init_dir: Path, root: Path):
    ref_path = ref.partition('#')[0]
    if find_file(ref_path, init_dir, root) is None:
        return f"file not found: '{ref_path}'"
    return None


def slo_names(documents: list) -> set:
    """SLO names from OpenSLO documents (kind: SLO) and from slos[] lists."""
    names = set()
    for document in documents:
        if not isinstance(document, dict):
            continue
        if document.get('kind') == 'SLO':
            names.add((document.get('metadata') or {}).get('name'))
        for item in document.get('slos') or []:
            if isinstance(item, dict):
                names.add(item.get('name'))
    return names


def check_slo_ref(ref: str, init_dir: Path, root: Path):
    ref_path, separator, name = ref.partition('#')
    path = find_file(ref_path, init_dir, root)
    if path is None:
        return f"SLO file not found: '{ref_path}'"
    if not separator:
        return None
    try:
        documents = load_documents(path)
    except yaml.YAMLError:
        return f"cannot parse SLO file: '{ref_path}'"
    if name not in slo_names(documents):
        return f"SLO '{name}' not found in '{ref_path}'"
    return None


def check_adr_ref(ref: str, init_dir: Path, root: Path, product: str):
    """An ADR is a path to a .md file or a full ID matching a file name in decisions/."""
    if ref.endswith('.md') or '/' in ref:
        if find_file(ref, init_dir, root) is None:
            return f"ADR file not found: '{ref}'"
        return None
    directories = [init_dir / 'decisions', root / 'products' / str(product) / 'decisions', root / 'decisions']
    if not any((directory / f'{ref}.md').is_file() for directory in directories):
        return f"ADR not found: '{ref}'"
    return None


def as_list(value) -> list:
    if not value:
        return []
    return value if isinstance(value, list) else [value]


def broken_links(req: dict, init_dir: Path, root: Path, product: str) -> list:
    """Return a description of every trace link of the requirement that does not resolve."""
    trace = req.get('trace') or {}
    problems = []
    for ref in as_list(trace.get('tests')):
        problems.append(check_test_ref(ref, req['id'], init_dir, root))
    for ref in as_list(trace.get('contracts')):
        problems.append(check_contract_ref(ref, init_dir, root))
    for field in ('schemas', 'architecture_views'):
        for ref in as_list(trace.get(field)):
            problems.append(check_file_ref(ref, init_dir, root))
    for ref in as_list(trace.get('slo')):
        problems.append(check_slo_ref(ref, init_dir, root))
    for ref in as_list(trace.get('adr')):
        problems.append(check_adr_ref(ref, init_dir, root, product))
    return [problem for problem in problems if problem]


def is_archived(metadata: dict) -> bool:
    return metadata.get('initiative_status') == 'archived'


def check_requirement_links(req_file: Path, root: Path, strict: bool, errors: list, warnings: list) -> tuple:
    """Check links and evidence of one requirements.yml. Returns (metadata, requirements)."""
    metadata, requirements = load_requirements(req_file)
    if is_archived(metadata):
        return metadata, []
    for req in requirements:
        status = req.get('status')
        terminal = status in TERMINAL_STATUSES
        for problem in broken_links(req, req_file.parent, root, metadata.get('product')):
            target = errors if terminal or strict else warnings
            label = 'ERROR' if target is errors else 'WARN'
            target.append(f"[{label}] {req_file}: {req['id']} ({status}): {problem}")
        if status != 'deprecated' and not has_evidence(req):
            target = errors if terminal else warnings
            label = 'ERROR' if terminal else 'WARN'
            target.append(
                f"[{label}] {req_file}: {req['id']} ({status}) has no trace evidence "
                f"(tests/contracts/slo are empty)"
            )
    return metadata, requirements


def run_checks(root: Path, strict: bool = False) -> tuple:
    """Run all checks. Returns (errors, warnings, l3_ref_count, l4_ref_count)."""
    errors = []
    warnings = []

    # Build L3 registry: {req_id: (requirement, profile)}
    registry = {}
    for req_file in root.glob('initiatives/*/requirements.yml'):
        if is_template(req_file.parent):
            continue
        try:
            metadata, requirements = check_requirement_links(req_file, root, strict, errors, warnings)
        except Exception as e:
            errors.append(f"[ERROR] Cannot parse {req_file}: {e}")
            continue
        for req in requirements:
            registry[req['id']] = (req, metadata.get('profile', 'minimal'))

    # Examples are checked for links only, their REQ-IDs do not join the registry
    for req_file in root.glob('examples/*/requirements.yml'):
        try:
            check_requirement_links(req_file, root, strict, errors, warnings)
        except Exception as e:
            errors.append(f"[ERROR] Cannot parse {req_file}: {e}")

    # Check REQ-IDs from L3 initiative trace.md files
    traced_req_ids = set()
    total_l3_req_refs = 0
    for trace_file in root.glob('initiatives/*/trace.md'):
        if is_template(trace_file.parent):
            continue
        req_yml = trace_file.parent / 'requirements.yml'
        if req_yml.exists():
            try:
                if is_archived(load_requirements(req_yml)[0]):
                    continue
            except Exception:
                pass
        try:
            l3_ids = parse_trace_md(trace_file)
            total_l3_req_refs += len(l3_ids)
            traced_req_ids.update(l3_ids)
            for req_id in l3_ids:
                if req_id not in registry:
                    errors.append(
                        f"[ERROR] {trace_file}: REQ-ID '{req_id}' not found "
                        f"in any initiatives/*/requirements.yml"
                    )
        except Exception as e:
            errors.append(f"[ERROR] Cannot parse {trace_file}: {e}")

    # Check L4 trace.md references exist in L3
    total_l4_req_refs = 0
    for trace_file in root.glob('.specify/specs/*/trace.md'):
        if is_template(trace_file.parent) or is_archived_spec(trace_file.parent, root):
            continue
        try:
            l4_req_ids = parse_trace_md(trace_file)
            total_l4_req_refs += len(l4_req_ids)
            traced_req_ids.update(l4_req_ids)
            for req_id in l4_req_ids:
                if req_id not in registry:
                    errors.append(
                        f"[ERROR] {trace_file}: REQ-ID '{req_id}' not found "
                        f"in any initiatives/*/requirements.yml"
                    )
        except Exception as e:
            errors.append(f"[ERROR] Cannot parse {trace_file}: {e}")

    # Check L3→L4 reverse: every REQ-ID from requirements.yml should appear in some trace.md
    for req_id, (req, profile) in registry.items():
        status = req.get('status')
        if req_id in traced_req_ids or status == 'deprecated':
            continue
        message = f"REQ-ID '{req_id}' ({status}) from requirements.yml has no entry in any trace.md (L3 or L4)"
        if status in TERMINAL_STATUSES and profile != 'minimal':
            errors.append(f"[ERROR] {message}")
        else:
            warnings.append(f"[WARN] {message}")

    return errors, warnings, total_l3_req_refs, total_l4_req_refs


def main():
    parser = argparse.ArgumentParser(description='Check REQ-ID consistency and trace links')
    parser.add_argument('--root', default='.', help='Repository root')
    parser.add_argument('--strict', action='store_true', help='Report broken links as errors for every status')
    args = parser.parse_args()

    errors, warnings, total_l3_req_refs, total_l4_req_refs = run_checks(Path(args.root), args.strict)

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
