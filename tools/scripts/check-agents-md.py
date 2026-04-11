#!/usr/bin/env python3
"""Validate AGENTS.md skill references against .claude/commands/.

Checks:
1. Every /speckit-* reference in AGENTS.md has a matching .claude/commands/<name>.md file
2. Every .claude/commands/speckit-*.md file is referenced in AGENTS.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Repository root")
    return parser.parse_args()


def extract_skill_refs(agents_md: str) -> set[str]:
    """Extract /speckit-* references from AGENTS.md."""
    pattern = re.compile(r"/speckit-([a-z0-9-]+)")
    return {m.group(1) for m in pattern.finditer(agents_md)}


def collect_command_files(root: Path) -> set[str]:
    """Collect speckit-*.md filenames from .claude/commands/."""
    commands_dir = root / ".claude" / "commands"
    if not commands_dir.exists():
        return set()
    names: set[str] = set()
    for f in sorted(commands_dir.glob("speckit-*.md")):
        # speckit-start.md -> start
        name = f.stem.replace("speckit-", "", 1)
        names.add(name)
    return names


def main() -> int:
    args = parse_args()
    root = Path(args.root)

    agents_file = root / "AGENTS.md"
    if not agents_file.exists():
        print("[WARN] AGENTS.md not found at repo root — skipping check")
        return 0

    agents_text = agents_file.read_text(encoding="utf-8")
    refs = extract_skill_refs(agents_text)
    files = collect_command_files(root)

    errors: list[str] = []

    # Check: every reference in AGENTS.md has a file
    missing_files = sorted(refs - files)
    for name in missing_files:
        errors.append(
            f"[ERROR] AGENTS.md references /speckit-{name} but "
            f".claude/commands/speckit-{name}.md does not exist"
        )

    # Check: every file is referenced in AGENTS.md
    missing_refs = sorted(files - refs)
    for name in missing_refs:
        errors.append(
            f"[ERROR] .claude/commands/speckit-{name}.md exists but "
            f"is not referenced in AGENTS.md"
        )

    for error in errors:
        print(error)

    if errors:
        print(f"\n❌ check-agents-md: {len(errors)} error(s)")
        return 1

    print(f"✅ check-agents-md: {len(refs)} skills in AGENTS.md, {len(files)} files — all match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
