---
description: Generate structured reflection and evolution proposals for a graduated initiative
argument-hint: <INIT-YYYY-NNN-slug> [--health]
---

You are generating a post-initiative reflection for `$ARGUMENTS`.

## Your job

### 1. Validate preconditions

1. Extract INIT-ID from `$ARGUMENTS` (strip `--health` flag if present).
2. Validate format: `^INIT-[0-9]{4}-[0-9]{3}-[a-z0-9-]+$`. If invalid → abort.
3. Check graduated status:
   - Read `initiatives/{INIT}/changelog/CHANGELOG.md` — must have at least one `## [x.y.z]` release entry beyond 0.1.0
   - OR read `initiatives/{INIT}/requirements.yml` — check `metadata.graduated: true`
   - If neither → error: "Initiative {INIT-ID} is not graduated. Run `/speckit-graduate` first."

### 2. Collect artifacts

1. **L3 artifacts:** Glob `initiatives/{INIT}/**/*` — list all files with relative paths
2. **L4 artifacts:** Search `.specify/specs/*/spec.md` for files containing the INIT-ID string. List matching spec directories.
3. **L5 artifacts:** Glob `evidence/*{INIT}*` (if `evidence/` exists). May be empty.

### 3. Usage analysis (per artifact)

For each collected artifact file:

1. **Updates count:**
   - If `.git` exists: `git log --oneline -- {file} | wc -l`
   - Fallback (no git): estimate from file size — >50 lines = likely multi-update, else 1
2. **Created date:**
   - If `.git` exists: `git log --reverse --format="%ai" -- {file} | head -1`
   - Fallback: file mtime
3. **Downstream references:**
   - `grep -rl "{filename}" --include="*.md" --include="*.yml" --include="*.yaml"` (excluding the file itself)
   - Count unique referencing files
4. **Verdict:**
   - `updates ≥ 2 AND downstream_refs ≥ 1` → **used**
   - `updates ≥ 1 AND downstream_refs = 0` → **underused**
   - `updates ≤ 1 AND downstream_refs = 0` → **unused**

### 4. Bottleneck analysis

Group artifacts by lifecycle phase:
- **Product:** `prd.md`, `requirements.yml`
- **Architecture:** `design.md`, `contracts/*`, `decisions/*`
- **Implementation:** `.specify/specs/*/tasks.md`, `.specify/specs/*/plan.md`, source files
- **Ops:** `ops/*`, `delivery/*`
- **Evidence:** `evidence/*`, `trace.md`

Per phase: sum `total_updates` across files, count `file_count`.
Flag as bottleneck if `total_updates > 3 × file_count`.

### 5. Generate findings

Based on verdicts and bottlenecks:
- **What worked:** List artifacts with verdict=used, especially those with high downstream refs
- **What was redundant:** List artifacts with verdict=unused — suggest review for template relevance
- **Recommendations:** Concrete, actionable suggestions based on patterns found

### 6. Generate evolution proposals

For each finding that implies a framework change (template improvement, constitution update, command modification):
1. Create proposal with fields: id, source_init, date, target_file, target_section, change_type, summary, rationale, diff_preview, status=proposed
2. ID generation: read `evolution-log.md` (if exists), find max EVOL-YYYY-NNN, increment. If file doesn't exist or is empty, start at EVOL-{YYYY}-001.
3. Append proposal rows to `evolution-log.md`

**CRITICAL CONSTRAINT (REQ-EVOL-005):** This command writes ONLY to:
- `initiatives/{INIT}/reflection.md` (new file)
- `evolution-log.md` (append rows only)

Do NOT modify constitution.md, templates/, or any .claude/commands/ file.

### 7. Render reflection.md

Use template from `templates/reflection-template.md`. Fill all 4 sections with computed data.
Write to `initiatives/{INIT}/reflection.md`.

### 8. Report

```
Reflection complete for {INIT-ID}

  Artifacts analyzed:  {count}
  Used:               {count}
  Underused:          {count}
  Unused:             {count}
  Bottleneck phases:  {list}
  Proposals generated: {count}

  Output: initiatives/{INIT}/reflection.md
  Proposals: evolution-log.md ({count} new rows)
```

## Rules
- ONLY analyze graduated initiatives — never generate reflection for active/draft work
- Use git history where available, degrade gracefully without it
- Proposals are ADVISORY — diff_preview is not executable, maintainer adapts when applying
- Keep reflection.md focused and factual — no speculation, base findings on data
- At least 1 evolution proposal per reflection (if any findings exist)
- Do NOT count TEMPLATE.md, protocol.md, or .gitignore as artifacts

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS | **Type:** utility | **Next:** _(preserve current)_
