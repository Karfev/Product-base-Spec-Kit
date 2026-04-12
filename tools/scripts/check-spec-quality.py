#!/usr/bin/env python3
"""Quality checks for .specify spec docs.

Checks files under .specify/specs/* (excluding template dirs containing `{...}`):
- prohibit unfilled template placeholders `{...}` in non-template specs,
- detect `[NEEDS CLARIFICATION]` entries with status `open` as warning/blocking,
- ensure `spec.md` has REQ-ID links and those IDs exist in `requirements.yml`,
- ensure `tasks.md` contains RED→GREEN sequence (T2a before T2b).
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQ_ID_PATTERN = re.compile(r"\bREQ-[A-Z0-9]+-\d{3}\b")
PLACEHOLDER_PATTERN = re.compile(r"\{([^{}\n]+)\}")
CLARIFICATION_OPEN_PATTERN = re.compile(
    r"\[NEEDS CLARIFICATION\].*\|\s*open\s*\|", re.IGNORECASE
)

TEMPLATE_HINTS = (
    "nnn",
    "slug",
    "yyyy",
    "init",
    "profile",
    "owner",
    "role",
    "capability",
    "benefit",
    "context",
    "action",
    "result",
)


def is_template(path: Path) -> bool:
    return "{" in str(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument(
        "--needs-clarification-policy",
        choices=("warning", "blocking"),
        default="blocking",
        help="How to treat [NEEDS CLARIFICATION] rows with status=open",
    )
    return parser.parse_args()


def is_unfilled_placeholder(token: str) -> bool:
    value = token.strip()
    lower = value.lower()

    if value in {"id", "name"}:
        return False

    if "…" in value or "..." in value:
        return True
    if any(ch in value for ch in ("|", "/", "@")):
        return True
    if ":" in value:
        return False
    if " " in value:
        return True
    if any(hint in lower for hint in TEMPLATE_HINTS):
        return True
    if re.search(r"\b[A-Z]{2,}(?:-[A-Z0-9]+)*\b", value):
        return True

    return False


def collect_yaml_req_ids(path: Path) -> set[str]:
    req_ids: set[str] = set()
    pattern = re.compile(r'^\s*-?\s*id:\s*["\']?(REQ-[A-Z0-9]+-\d{3})["\']?\s*$')
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            req_ids.add(match.group(1))
    return req_ids


def collect_all_yaml_req_ids(root: Path) -> set[str]:
    """Collect REQ-IDs from ALL initiatives' requirements.yml files."""
    all_ids: set[str] = set()
    initiatives_dir = root / "initiatives"
    if not initiatives_dir.exists():
        return all_ids
    for req_file in sorted(initiatives_dir.glob("*/requirements.yml")):
        if "{" in str(req_file):
            continue
        all_ids |= collect_yaml_req_ids(req_file)
    return all_ids


def parse_initiative_id(spec_text: str) -> str | None:
    match = re.search(r"^\*\*Initiative:\*\*\s*([^\s]+)", spec_text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def is_archived_initiative(init_id: str | None, root: Path) -> bool:
    """Check if the initiative is archived."""
    if not init_id:
        return False
    try:
        import yaml
        req_yml = root / "initiatives" / init_id / "requirements.yml"
        if req_yml.exists():
            with open(req_yml) as f:
                data = yaml.safe_load(f)
            return data.get("metadata", {}).get("initiative_status") == "archived"
    except Exception:
        pass
    return False


def main() -> int:
    args = parse_args()
    root = Path(args.root)

    errors: list[str] = []
    warnings: list[str] = []

    for spec_dir in sorted((root / ".specify" / "specs").glob("*")):
        if not spec_dir.is_dir() or is_template(spec_dir):
            continue

        spec_md = spec_dir / "spec.md"
        tasks_md = spec_dir / "tasks.md"

        if not spec_md.exists():
            errors.append(f"[ERROR] {spec_md}: missing file")
            continue
        if not tasks_md.exists():
            plan_md = spec_dir / "plan.md"
            if plan_md.exists():
                errors.append(
                    f"[ERROR] {tasks_md}: missing file "
                    f"(plan.md exists — run /speckit-tasks)"
                )
            else:
                warnings.append(
                    f"[WARN] {tasks_md}: not yet created "
                    f"(run /speckit-plan then /speckit-tasks)"
                )
            continue

        spec_text = spec_md.read_text(encoding="utf-8")

        # Skip specs whose parent initiative is archived.
        init_id_early = parse_initiative_id(spec_text)
        if is_archived_initiative(init_id_early, root):
            continue

        # 1) Unfilled placeholders in non-template specs.
        in_code_block = False
        for line_no, line in enumerate(spec_text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            if "<!--" in line and "-->" in line:
                continue
            for match in PLACEHOLDER_PATTERN.finditer(line):
                token = match.group(1)
                if is_unfilled_placeholder(token):
                    errors.append(
                        f"[ERROR] {spec_md}:{line_no}: unfilled placeholder '{{{token}}}'"
                    )

        # 2) Open clarifications.
        for line_no, line in enumerate(spec_text.splitlines(), start=1):
            if CLARIFICATION_OPEN_PATTERN.search(line):
                message = (
                    f"[WARNING] {spec_md}:{line_no}: [NEEDS CLARIFICATION] has status=open"
                )
                if args.needs_clarification_policy == "blocking":
                    errors.append(message.replace("[WARNING]", "[ERROR]"))
                else:
                    warnings.append(message)

        # 3) REQ-ID links in spec.md and existence in requirements.yml.
        spec_req_ids = set(REQ_ID_PATTERN.findall(spec_text))
        if not spec_req_ids:
            errors.append(f"[ERROR] {spec_md}: no REQ-ID references found")

        # Collect REQ-IDs from ALL initiatives to support cross-initiative references.
        all_yaml_req_ids = collect_all_yaml_req_ids(root)
        missing = sorted(spec_req_ids - all_yaml_req_ids)
        if missing:
            errors.append(
                f"[ERROR] {spec_md}: REQ-ID(s) missing in any initiatives/*/requirements.yml: {', '.join(missing)}"
            )

        # 4) Check contract files for unfilled placeholders (warning only).
        initiative_id = parse_initiative_id(spec_text)
        if initiative_id:
            initiative_dir = root / "initiatives" / initiative_id
            contracts_dir = initiative_dir / "contracts"
            if contracts_dir.exists():
                for contract_file in sorted(contracts_dir.glob("*.yaml")):
                    if is_template(contract_file):
                        continue
                    contract_text = contract_file.read_text(encoding="utf-8")
                    for line_no, line in enumerate(contract_text.splitlines(), start=1):
                        if "<!--" in line and "-->" in line:
                            continue
                        for match in PLACEHOLDER_PATTERN.finditer(line):
                            token = match.group(1)
                            if is_unfilled_placeholder(token):
                                warnings.append(
                                    f"[WARNING] {contract_file}:{line_no}: unfilled placeholder '{{{token}}}' in contract"
                                )

        # 5) RED -> GREEN sequence in tasks.md: T2a before T2b.
        tasks_text = tasks_md.read_text(encoding="utf-8")
        t2a_match = re.search(r"\bT2a\b", tasks_text)
        t2b_match = re.search(r"\bT2b\b", tasks_text)

        if not t2a_match or not t2b_match:
            errors.append(
                f"[ERROR] {tasks_md}: required RED→GREEN tasks missing (need T2a and T2b)"
            )
        elif t2a_match.start() > t2b_match.start():
            errors.append(
                f"[ERROR] {tasks_md}: RED→GREEN sequence invalid (T2a must come before T2b)"
            )

        # 5b) Task ordering enforcement (REQ-QUAL-005):
        # Detect T2b checkbox marked done without T2a marked done.
        if t2a_match and t2b_match:
            t2a_done = re.search(r"-\s*\[x\]\s*\*\*T2a\b", tasks_text, re.IGNORECASE)
            t2b_done = re.search(r"-\s*\[x\]\s*\*\*T2b\b", tasks_text, re.IGNORECASE)
            if t2b_done and not t2a_done:
                warnings.append(
                    f"[WARN] {tasks_md}: T2b marked done but T2a not done "
                    f"— tests should be written before implementation (AI Quality Gates Pillar 2)"
                )

    for warning in warnings:
        print(warning)
    for error in errors:
        print(error)

    if errors:
        print(f"\n❌ check-spec-quality: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"✅ check-spec-quality: passed with {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
