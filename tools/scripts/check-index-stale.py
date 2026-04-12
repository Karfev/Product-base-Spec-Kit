#!/usr/bin/env python3
"""Check if requirements-index.md and contracts-index.md are stale.

Compares the source-hash in the index file header against the current
SHA-256 hash of the source file. Emits warnings (non-blocking) for
stale indexes.
"""

import hashlib
import re
import sys
from pathlib import Path


def compute_hash(filepath: Path) -> str:
    """Return first 12 chars of SHA-256 hash of file contents."""
    return hashlib.sha256(filepath.read_bytes()).hexdigest()[:12]


def extract_hash(index_path: Path):
    """Extract source-hash from HTML comment header."""
    try:
        first_line = index_path.read_text().split("\n")[0]
        match = re.search(r"source-hash:\s*(\w+)", first_line)
        return match.group(1) if match else None
    except (FileNotFoundError, IndexError):
        return None


def check_initiative(init_dir: Path) -> list[str]:
    """Check one initiative directory for stale indexes."""
    warnings = []

    # Check requirements-index.md
    req_yml = init_dir / "requirements.yml"
    req_idx = init_dir / "requirements-index.md"
    if req_yml.exists() and req_idx.exists():
        current = compute_hash(req_yml)
        stored = extract_hash(req_idx)
        if stored and current != stored:
            warnings.append(
                f"  WARNING: {req_idx} is stale "
                f"(stored={stored}, current={current}). "
                f"Run /speckit-requirements to regenerate."
            )

    # Check contracts-index.md
    openapi = init_dir / "contracts" / "openapi.yaml"
    contracts_idx = init_dir / "contracts" / "contracts-index.md"
    if openapi.exists() and contracts_idx.exists():
        current = compute_hash(openapi)
        stored = extract_hash(contracts_idx)
        if stored and current != stored:
            warnings.append(
                f"  WARNING: {contracts_idx} is stale "
                f"(stored={stored}, current={current}). "
                f"Run /speckit-contracts to regenerate."
            )

    return warnings


def main():
    initiatives_dir = Path("initiatives")
    if not initiatives_dir.exists():
        print("  No initiatives/ directory found — skipping")
        return

    all_warnings = []
    for init_dir in sorted(initiatives_dir.iterdir()):
        if not init_dir.is_dir() or "{" in init_dir.name:
            continue
        all_warnings.extend(check_initiative(init_dir))

    if all_warnings:
        for w in all_warnings:
            print(w)
        print(f"\n  {len(all_warnings)} stale index(es) found (warning only)")
    else:
        print("  All indexes up-to-date (or no indexes found)")


if __name__ == "__main__":
    main()
