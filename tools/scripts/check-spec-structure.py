#!/usr/bin/env python3
"""Validate minimal structure for .specify spec docs.

Checks files under .specify/specs/* for required headings in:
- spec.md
- plan.md
- tasks.md

Template directories containing {...} are skipped.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = {
    "spec.md": [
        "Summary",
        "Requirements",
        "Acceptance criteria",
    ],
    "plan.md": [
        "Contracts impact",
        "Test strategy",
        "Rollout & rollback",
    ],
    "tasks.md": [
        "Task list",
    ],
}

HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+?)\s*$")


def is_template(path: Path) -> bool:
    """Skip template placeholder directories containing {braces}."""
    return "{" in str(path)


def normalize_heading(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def extract_headings(path: Path) -> set[str]:
    headings: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_PATTERN.match(line)
        if not match:
            continue
        headings.add(normalize_heading(match.group(1)))
    return headings


def main() -> int:
    root = Path(".")
    if "--root" in sys.argv:
        idx = sys.argv.index("--root")
        try:
            root = Path(sys.argv[idx + 1])
        except IndexError:
            print("[ERROR] --root requires a path argument")
            return 1

    errors: list[str] = []

    for spec_dir in sorted((root / ".specify" / "specs").glob("*")):
        if not spec_dir.is_dir() or is_template(spec_dir):
            continue

        for filename, required in REQUIRED_HEADINGS.items():
            doc_path = spec_dir / filename
            if not doc_path.exists():
                errors.append(f"[ERROR] {doc_path}: missing file")
                continue

            headings = extract_headings(doc_path)
            for heading in required:
                if normalize_heading(heading) not in headings:
                    errors.append(
                        f"[ERROR] {doc_path}: missing heading '## {heading}'"
                    )

    for error in errors:
        print(error)

    if errors:
        print(f"\n❌ check-spec-structure: {len(errors)} error(s)")
        return 1

    print("✅ check-spec-structure: all required headings are present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
