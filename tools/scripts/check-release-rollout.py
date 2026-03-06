#!/usr/bin/env python3
"""Validate consistency between delivery rollout docs and ops readiness artifacts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check rollout/migration consistency with SLO + PRR docs"
    )
    parser.add_argument(
        "--initiative",
        dest="initiative",
        help="Specific initiative ID (e.g., INIT-2026-000-api-key-management)",
    )
    return parser.parse_args()


def list_initiatives(base: Path, only: str | None) -> list[Path]:
    if only:
        candidate = base / only
        return [candidate] if candidate.is_dir() else []

    return sorted(
        p
        for p in base.iterdir()
        if p.is_dir() and not p.name.startswith("{") and p.name.startswith("INIT-")
    )


def parse_profile(requirements_file: Path) -> str:
    if not requirements_file.exists():
        return "standard"

    for line in requirements_file.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*profile:\s*\"?([a-zA-Z]+)\"?", line)
        if m:
            return m.group(1).strip().lower()
    return "standard"


def extract_slo_ids(slo_file: Path) -> list[str]:
    if not slo_file.exists():
        return []

    text = slo_file.read_text(encoding="utf-8")
    docs = re.split(r"\n---\n", text)
    ids: list[str] = []
    for doc in docs:
        if re.search(r"^kind:\s*SLO\s*$", doc, flags=re.MULTILINE) is None:
            continue
        m = re.search(r"^\s*name:\s*([a-zA-Z0-9_.-]+)\s*$", doc, flags=re.MULTILINE)
        if m:
            ids.append(m.group(1))
    return ids


def check_initiative(initiative_dir: Path) -> tuple[list[str], bool]:
    errors: list[str] = []
    req_file = initiative_dir / "requirements.yml"
    profile = parse_profile(req_file)

    rollout_file = initiative_dir / "delivery" / "rollout.md"
    prr_file = initiative_dir / "ops" / "prr-checklist.md"
    slo_file = initiative_dir / "ops" / "slo.yaml"

    has_release_artifacts = rollout_file.exists() or prr_file.exists() or slo_file.exists()
    if not has_release_artifacts:
        return errors, False

    if not rollout_file.exists():
        errors.append("delivery/rollout.md is missing")
        return errors, True

    rollout_text = rollout_file.read_text(encoding="utf-8")
    rollout_lower = rollout_text.lower()

    if "feature flag" not in rollout_lower and "feature-flag" not in rollout_lower:
        errors.append("rollout.md does not describe a feature flag")

    if "триггер для отката" not in rollout_lower and "rollback trigger" not in rollout_lower:
        errors.append("rollout.md does not contain rollback trigger section")

    slo_ids = extract_slo_ids(slo_file)
    for slo_id in slo_ids:
        if slo_id not in rollout_text and f"ops/slo.yaml#{slo_id}" not in rollout_text:
            errors.append(f"rollout.md does not reference SLO '{slo_id}' from ops/slo.yaml")

    if not prr_file.exists():
        errors.append("ops/prr-checklist.md is missing")
    else:
        prr_text = prr_file.read_text(encoding="utf-8").lower()
        if "delivery/rollout.md" not in prr_text:
            errors.append("prr-checklist.md does not reference delivery/rollout.md")
        if "feature flag" not in prr_text and "feature flags" not in prr_text:
            errors.append("prr-checklist.md does not mention feature flags")

    if profile in {"extended", "enterprise"}:
        migration_file = initiative_dir / "delivery" / "migration.md"
        if not migration_file.exists():
            errors.append("delivery/migration.md is required for Extended/Enterprise profiles")
        else:
            migration_text = migration_file.read_text(encoding="utf-8")
            if "rollback" not in migration_text.lower():
                errors.append("migration.md must contain rollback section")

    return errors, True


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[2]
    initiatives_root = repo_root / "initiatives"

    initiatives = list_initiatives(initiatives_root, args.initiative)
    if args.initiative and not initiatives:
        print(f"[ERROR] Initiative not found: {args.initiative}")
        return 1

    failures = 0
    for initiative_dir in initiatives:
        errs, checked = check_initiative(initiative_dir)
        if not checked:
            print(f"[SKIP] {initiative_dir.name} (no release artifacts)")
            continue
        if errs:
            failures += 1
            print(f"[FAIL] {initiative_dir.name}")
            for err in errs:
                print(f"  - {err}")
        else:
            print(f"[OK] {initiative_dir.name}")

    if failures:
        print(f"\nRelease rollout consistency check failed for {failures} initiative(s).")
        return 1

    print("\nRelease rollout consistency check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
