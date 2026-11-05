#!/usr/bin/env python3
"""
Find requirement conflicts before graduation: compare the deltas of active initiatives
with products/<product>/requirements-registry.yml, using the rules of graduate.py.

Severity (status of the requirement):
  implemented, verified, or deprecated with delta: removed — a conflict is an error
  other statuses                                           — a conflict is a warning

Two active initiatives that change one requirement are reported as a warning: the
first to graduate wins, the second then has to rebase onto the new rev.

Initiatives with graduated: true or initiative_status: archived are skipped.

Usage:
  python tools/scripts/check-deltas.py [--root <path>]

Exit codes:
  0 — no errors (warnings may be printed)
  1 — errors found
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import graduate  # noqa: E402


def load_registry_entries(path: Path, errors: list) -> dict:
    """Returns {req_id: entry}, reporting problems of the registry itself."""
    try:
        _, registry = graduate.load_registry(path)
    except graduate.RegistrySchemaError as error:
        errors.append(f"[ERROR] REGISTRY_SCHEMA: {error}")
        return {}
    entries = {}
    for entry in (registry or {}).get('entries') or []:
        entries[entry['id']] = entry
        history = entry.get('history') or []
        if not history or history[-1].get('rev') != entry.get('rev'):
            errors.append(
                f"[ERROR] REGISTRY_HISTORY: {path}: {entry['id']} is at rev {entry.get('rev')}, "
                f"its history ends at rev {history[-1].get('rev') if history else None}"
            )
    return entries


def is_blocking(req: dict) -> bool:
    if req.get('delta') == 'removed':
        return req.get('status') == 'deprecated'
    return req.get('status') in graduate.ELIGIBLE_STATUSES


def run_checks(root: Path) -> tuple:
    """Returns (errors, warnings)."""
    errors = []
    warnings = []
    registries = {
        path.parent.name: load_registry_entries(path, errors)
        for path in sorted(root.glob('products/*/requirements-registry.yml'))
        if '{' not in str(path)
    }

    changes = {}
    for req_file in sorted(root.glob('initiatives/*/requirements.yml')):
        if '{' in str(req_file.parent):
            continue
        try:
            metadata, requirements = graduate.load_initiative(req_file)
        except Exception as e:
            errors.append(f"[ERROR] Cannot parse {req_file}: {e}")
            continue
        if metadata.get('graduated') or metadata.get('initiative_status') == 'archived':
            continue
        name = req_file.parent.name
        product = metadata.get('product')
        entries = registries.get(product, {})
        for req in requirements:
            action, problem = graduate.classify(req, entries.get(req['id']), name, ignore_status=True)
            if action == 'noop':
                continue
            changes.setdefault((product, req['id']), []).append(name)
            if action == 'conflict':
                target, label = (errors, 'ERROR') if is_blocking(req) else (warnings, 'WARN')
                target.append(
                    f"[{label}] {problem['code']}: {req_file}: {problem['message']} ({req.get('status')}). "
                    f"Fix: {problem['fix']}"
                )

    for (product, req_id), initiatives in sorted(changes.items()):
        if len(initiatives) > 1:
            warnings.append(
                f"[WARN] PARALLEL_CHANGE: {req_id} in product {product} is changed by "
                f"{', '.join(initiatives)}. The first to graduate wins, the others rebase."
            )
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description='Find requirement conflicts before graduation')
    parser.add_argument('--root', default='.', help='Repository root')
    args = parser.parse_args()

    errors, warnings = run_checks(Path(args.root))
    for message in warnings + errors:
        print(message)
    if errors:
        print(f"\n❌ check-deltas: {len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(1)
    print(f"{'⚠️ ' if warnings else '✅'} check-deltas: 0 errors, {len(warnings)} warning(s)")


if __name__ == '__main__':
    main()
