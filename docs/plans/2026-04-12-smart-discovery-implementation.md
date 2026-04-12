# Smart Discovery Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add auto-routing and codebase-first context loading to SpecKit, reducing time-to-first-validate from ~45 min to ~15 min (Minimal).

**Architecture:** Unified flow through `/speckit-start` with three new components: (1) auto-routing engine using risk-keywords.yml, (2) codebase-first context loading in `/speckit-prd`, (3) depth modes. `/speckit-quick` is a standalone shortcut that delegates to the same flow.

**Tech Stack:** Claude Code skills (.md command files), YAML config, Python validation scripts.

**Design doc:** `docs/plans/2026-04-12-smart-discovery-design.md`

**Initiative:** INIT-2026-006-smart-discovery

---

### Task 1: Create risk-keywords.yml

**Files:**
- Create: `.specify/memory/risk-keywords.yml`

**Step 1: Create risk-keywords dictionary**

```yaml
# Risk-keyword dictionary for auto-routing engine.
# Used by /speckit-quick and /speckit-start to determine initiative profile.
# Canonical source of truth for risk-keyword detection (REQ-DISC-002).

high_risk:
  - pattern: "auth|authentication|JWT|OAuth|OIDC|авториз"
    min_profile: standard
    reason: "Authentication affects security posture"
  - pattern: "PII|GDPR|ПДн|152-ФЗ|персональн"
    min_profile: extended
    reason: "PII/GDPR requires threat model + compliance review"
  - pattern: "payment|billing|платёж|тариф"
    min_profile: standard
    reason: "Financial transactions require audit trail"
  - pattern: "migration|миграц"
    min_profile: standard
    reason: "Data migrations require rollback strategy"
  - pattern: "breaking.?change|ломающ"
    min_profile: standard
    reason: "Breaking changes require deprecation process"
  - pattern: "public.?API|внешн.{0,5}API"
    min_profile: standard
    reason: "Public APIs require contract compatibility"
  - pattern: "SLA|SLO"
    min_profile: standard
    reason: "SLA commitments require SLO definition"

medium_risk:
  - pattern: "API|REST|endpoint"
  - pattern: "event|async|kafka|rabbitmq"
  - pattern: "database|schema|таблиц"
  - pattern: "contract|контракт"
  - pattern: "deploy|rollback|canary"
  - pattern: "сервис|microservice"
  - pattern: "очеред|queue"

# Component-count keywords (for STEP 2 of routing algorithm)
component_indicators:
  - "файл"
  - "компонент"
  - "сервис"
  - "endpoint"
  - "таблица"
  - "модуль"
  - "контракт"
```

**Step 2: Validate YAML syntax**

Run: `python3 -c "import yaml; yaml.safe_load(open('.specify/memory/risk-keywords.yml'))"`
Expected: No output (valid YAML)

**Step 3: Commit**

```bash
git add .specify/memory/risk-keywords.yml
git commit -m "feat(006): add risk-keywords.yml — auto-routing dictionary (REQ-DISC-002)"
```

---

### Task 2: Create /speckit-quick command

**Files:**
- Create: `.claude/commands/speckit-quick.md`

**Step 1: Create the command file**

The command is a standalone shortcut. It:
1. Asks for a task description
2. Reads `.specify/memory/risk-keywords.yml`
3. Runs the routing algorithm (regex match on description)
4. Suggests profile with risk warnings
5. If Minimal → scaffolds immediately via init.sh
6. Otherwise → asks user to confirm/override/run full /speckit-profile

```markdown
---
description: Express initiative creation — auto-detect profile from task description
argument-hint: [description] (e.g., "fix typo in README" or "add JWT auth to API")
---

You are the SpecKit quick-start guide. Your goal: auto-detect the initiative profile from a task description and scaffold in under 5 minutes.

## Your job

1. **Get task description.**
   If `$ARGUMENTS` is provided and is NOT an INIT-ID (doesn't match `^INIT-`), use it as the description.
   Otherwise ask: "Опиши задачу в 1-2 предложениях:"

2. **Read risk-keywords dictionary.**
   Read `.specify/memory/risk-keywords.yml` — load `high_risk`, `medium_risk`, and `component_indicators` lists.

3. **Run auto-routing algorithm:**

   **STEP 1 — Risk-keyword scan (case-insensitive):**
   - For each `high_risk` entry: check if `pattern` matches the description (regex, case-insensitive)
   - For each `medium_risk` entry: check if `pattern` matches
   - If ANY high_risk matched → `profile = max(kw.min_profile)` across all matches
   - Else if ≥3 medium_risk matched → `profile = "standard"`
   - Else → `profile = "minimal"`

   **STEP 2 — Component count estimation:**
   - Count mentions of `component_indicators` words in description
   - If >15 mentions → `profile = max(profile, "extended")`
   - If >5 mentions → `profile = max(profile, "standard")`

   Profile ordering for `max()`: minimal < standard < extended < enterprise

4. **Present result:**

   **If profile = "minimal" AND no high_risk matches:**
   ```
   🎯 Auto-routing: Minimal
   Причина: простая задача без risk-keywords.

   Переходим к scaffold? [Да / Переопределить профиль / Пройти /speckit-profile]
   ```
   If user confirms → proceed to step 5 (scaffold).

   **If profile = "standard" or higher:**
   ```
   🎯 Auto-routing: {Profile}
   Обнаружены risk-keywords:
   - "{matched_pattern}" → {reason}
   - "{matched_pattern}" → {reason}

   Подтвердить профиль {Profile}? [Да / Переопределить / Пройти /speckit-profile]
   ```
   If user chooses "Переопределить" → ask which profile they want.
   If user chooses "/speckit-profile" → suggest running `/speckit-profile` for full risk assessment.

5. **Scaffold the initiative:**
   - Ask Q1 (slug), Q5 (product) from `/speckit-start` flow if not already known
   - Determine INIT-ID: `INIT-{YYYY}-{NNN}-{slug}` where NNN = next available
   - Run scaffold equivalent to: `./tools/init.sh {INIT-ID} {NNN}-{slug} --profile {profile} --product {product}`
   - If the determined profile is Standard+, scaffold includes design.md, contracts/, ops/ etc.

6. **Transition to PRD:**
   - Say: "Scaffold создан. Переходим к PRD."
   - The description from step 1 can pre-fill the Problem and Outcome fields in PRD
   - Suggest: `Run /speckit-prd {INIT-ID} to fill the PRD with codebase-first context`

## Override handling (REQ-DISC-006)

- **Override UP** (e.g., Minimal → Standard): inform user that additional artifacts will be created (design.md, contracts/, ops/). Proceed with the higher profile.
- **Override DOWN** (e.g., Standard → Minimal): if high_risk keywords were detected, show warning: "⚠️ Обнаружены risk-keywords ({list}). Понижение профиля может привести к пропуску важных артефактов. Подтверждаете?" Proceed only after explicit confirmation.

## Rules
- ALWAYS offer escape to `/speckit-profile` for full risk assessment
- Auto-routing is a HEURISTIC — never override user's explicit choice
- Keep interaction under 2 minutes for Minimal profile
- If user provides an INIT-ID as argument instead of description, inform them: "Для существующей инициативы используйте `/speckit-start {INIT-ID}` или `/speckit-profile {INIT-ID}`"
- risk-keywords.yml is the SINGLE source of truth for keyword patterns — do NOT hardcode patterns
```

**Step 2: Verify file is valid markdown**

Run: `head -5 .claude/commands/speckit-quick.md`
Expected: Shows frontmatter with description and argument-hint.

**Step 3: Commit**

```bash
git add .claude/commands/speckit-quick.md
git commit -m "feat(006): add /speckit-quick — auto-routing command (REQ-DISC-001, REQ-DISC-006)"
```

---

### Task 3: Modify /speckit-start — add routing choice

**Files:**
- Modify: `.claude/commands/speckit-start.md`

**Step 1: Add Step 0 routing choice**

Replace the current Step 1 "Welcome & context check" section (lines 10-12) with an expanded flow that adds a routing choice before the existing 5 questions.

Current (lines 6-12):
```markdown
You are the SpecKit onboarding guide. Your goal: take a new user from zero to a validated Minimal initiative in under 30 minutes.

## Your job

1. **Welcome & context check.**
   Say: "Welcome to SpecKit! I'll help you create your first spec-validated initiative in about 10 minutes."
   Check if `initiatives/` has any existing initiatives. If yes, mention them for context.
```

New:
```markdown
You are the SpecKit onboarding guide. Your goal: take a new user from zero to a validated initiative in under 30 minutes.

## Your job

0. **Welcome & routing choice.**
   Say: "Welcome to SpecKit! I'll help you create a spec-validated initiative."
   Check if `initiatives/` has any existing initiatives. If yes, mention them for context.

   Ask: "Как хочешь начать?"
   - **a) "Опиши задачу в 1-2 предложениях"** → run auto-routing (see Step 0a below)
   - **b) "Пройти risk assessment"** → suggest: "Run `/speckit-profile` for full 8-question risk assessment"
   - **c) "Я знаю профиль: <minimal|standard|extended>"** → use that profile directly, skip to Step 1

   **Step 0a — Auto-routing (if user chose option a):**
   1. Read `.specify/memory/risk-keywords.yml`
   2. Run the routing algorithm from the design doc (see `/speckit-quick` for full algorithm):
      - Scan high_risk patterns → if match → suggest min_profile with risk warnings
      - Scan medium_risk patterns → if ≥3 matches → suggest standard
      - Estimate component count → adjust profile if needed
   3. Present result:
      - If Minimal + no high_risk: "🎯 Профиль: Minimal. Переходим к вопросам."
      - If Standard+: show risk warnings, ask to confirm/override/run /speckit-profile
   4. Set `{profile}` for scaffolding in Step 3.
   5. Use the task description to pre-fill Q2 (Problem) and Q3 (Outcome) where possible.

1. **Collect answers** (ask one at a time, skip if pre-filled from Step 0a):
```

Also update Step 3 (scaffolding, line 31-35) to use the determined profile instead of hardcoded "minimal":

Current:
```
./tools/init.sh INIT-{...} {NNN}-{slug} --profile minimal --product {answer5}
```

New:
```
./tools/init.sh INIT-{...} {NNN}-{slug} --profile {profile} --product {answer5}
```

And update the Rules section (line 123-132) — remove the rule "ALWAYS use Minimal profile" and replace with:

Current (line 125):
```
- ALWAYS use Minimal profile. If user wants Standard+, say: "Let's start with Minimal..."
```

New:
```
- Default to Minimal profile unless auto-routing or user choice determines otherwise.
- If auto-routing suggests Standard+, scaffold with that profile's full artifact set.
```

**Step 2: Verify no syntax issues**

Run: `head -30 .claude/commands/speckit-start.md`
Expected: Shows updated Step 0 with routing choice.

**Step 3: Commit**

```bash
git add .claude/commands/speckit-start.md
git commit -m "feat(006): add routing choice to /speckit-start — quick/profile/explicit (REQ-DISC-001)"
```

---

### Task 4: Modify /speckit-prd — add depth modes

**Files:**
- Modify: `.claude/commands/speckit-prd.md`

**Step 1: Add depth mode determination**

After current step 3 (line 13, reading constitution.md), add a new step that determines discovery depth based on the initiative profile:

Insert after line 3 ("Read `.specify/memory/constitution.md`..."):

```markdown
3b. **Determine discovery depth mode:**
   Read the `profile` field from `initiatives/$ARGUMENTS/requirements.yml` metadata.
   Map profile to depth:
   - `minimal` → **Quick mode** (3-5 questions): Problem, Scope, REQs, Risks (optional), Metrics (optional)
   - `standard` → **Standard mode** (5-10 questions): Quick + Users/Scenarios, Architecture constraints, Contract changes, NFR targets vs L2 baseline, Dependencies
   - `extended` or `enterprise` → **Deep mode** (10-15 questions): Standard + Security/threat model, Compliance, Migration strategy, Rollout constraints, Cross-initiative impact

   If `$ARGUMENTS` contains `--depth quick|standard|deep`, use that override regardless of profile.

   Announce the mode: "Discovery mode: {Quick|Standard|Deep} ({N} вопросов по профилю {profile})"
```

**Step 2: Update the question list to be depth-aware**

Replace current step 5 (lines 38-44) with depth-aware question selection:

Current:
```markdown
5. Ask the user **5 structured questions** (skip if already answered in existing prd.md):

   - **Problem:** What specific problem does this solve?...
   - **Why now:** What is the urgency driver...
   - **Primary personas:** Who are the users?...
   - **Scope:** What is explicitly IN-scope and OUT-of-scope...
   - **Success metrics:** What measurable outcomes define success?...
```

New:
```markdown
5. **Ask questions based on depth mode** (skip if already answered in existing prd.md):

   **Quick mode (3-5 questions) — Minimal profile:**
   - Q1 **Problem + Outcome:** What problem does this solve and what does success look like?
   - Q2 **Scope:** What is IN-scope? (2-4 items → maps to REQ-IDs)
   - Q3 **Risks:** Top risk? (optional — skip if user says "none")
   - Q4 **Metrics:** One key success metric? (optional — skip if user says "later")

   **Standard mode (5-10 questions) — Standard profile:**
   All Quick questions, plus:
   - Q5 **Why now:** Urgency driver — deadline, revenue risk, regulatory, competitive?
   - Q6 **Primary personas:** Who are the users? (role + JTBD format)
   - Q7 **Architecture constraints:** Any technology/stack constraints? (check L2 architecture first)
   - Q8 **Contract changes:** Does this add or change API endpoints or events?
   - Q9 **NFR targets:** Any latency, throughput, or availability requirements? (check L2 NFR baseline first)
   - Q10 **Dependencies:** Any upstream/downstream service dependencies?

   **Deep mode (10-15 questions) — Extended/Enterprise profile:**
   All Standard questions, plus:
   - Q11 **Security scope:** Authentication/authorization changes? Data classification?
   - Q12 **Compliance:** Regulatory requirements (GDPR, SOC2, PCI-DSS)?
   - Q13 **Migration:** Data migration or schema changes needed?
   - Q14 **Rollout constraints:** Feature flags? Canary? Regional rollout?
   - Q15 **Cross-initiative impact:** Does this affect other active initiatives?
```

**Step 3: Commit**

```bash
git add .claude/commands/speckit-prd.md
git commit -m "feat(006): add depth modes to /speckit-prd — Quick/Standard/Deep (REQ-DISC-005)"
```

---

### Task 5: Modify /speckit-prd — add codebase-first context loading

**Files:**
- Modify: `.claude/commands/speckit-prd.md`

**Step 1: Add context loading logic**

Insert a new section after step 4c (product contract registry scan, line 36) and before step 5 (questions):

```markdown
4d. **Codebase-first context loading (REQ-DISC-003, REQ-DISC-004):**

   Before each PRD question, scan existing L1/L2/L3 artifacts for relevant context.
   Use this mapping to determine which files to check:

   | Question topic | Files to check | Section to extract |
   |---|---|---|
   | Problem / Outcome | Last 3 active L3 `initiatives/*/prd.md` (by last_updated) | "Цель и ожидаемый эффект" |
   | Architecture / Tech stack | `products/{product}/architecture/overview.md` | Technology, Stack, Components |
   | NFR targets | `products/{product}/nfr-baseline/baseline.md` | All measurable targets |
   | Terminology | `domains/*/glossary.md` (all domains) | All terms |
   | API patterns | Last 3 active L3 `initiatives/*/contracts/openapi.yaml` | paths section |
   | Users / Scenarios | Last 3 active L3 `initiatives/*/prd.md` | "Пользователи и сценарии" |
   | Security | Active L3 `initiatives/*/ops/threat-model.md` | Threats, Mitigations |
   | Compliance | `domains/*/regulatory/` (if exists) | All |

   **Loading rules:**
   - Max 3 files per question (sorted by `last_updated` desc if metadata available, else by filename desc)
   - Skip archived initiatives (`initiative_status == "archived"` in requirements.yml)
   - Skip template directories (containing `{` in path)
   - If a file doesn't exist at the expected path → silently skip

   **Proposed answer format:**
   If relevant context is found, present it BEFORE asking the question:
   ```
   📋 Контекст из репозитория:
   Предположительно: {extracted_content}
   (источник: {relative_path})
   Верно? [Да / Нет / Уточнить]
   ```

   If the source file's `last_updated` or git modification date is > 90 days old:
   ```
   ⚠️ Источник обновлён > 90 дней назад — проверьте актуальность
   ```

   **User responses:**
   - **Да** → use the proposed answer as-is, write it into prd.md, move to next question
   - **Нет** → discard the proposed answer, ask the question as open-ended
   - **Уточнить** → use the proposed answer as a starting point, ask user to modify

   **If no relevant context found** → ask the question as open-ended (current behavior, no change).
```

**Step 2: Commit**

```bash
git add .claude/commands/speckit-prd.md
git commit -m "feat(006): add codebase-first context loading to /speckit-prd (REQ-DISC-003, REQ-DISC-004)"
```

---

### Task 6: Update documentation

**Files:**
- Modify: `.specify/memory/constitution.md`
- Modify: `initiatives/INIT-2026-006-smart-discovery/changelog/CHANGELOG.md`

**Step 1: Update constitution.md — add /speckit-quick to skill ordering**

In `.specify/memory/constitution.md`, find the "Порядок навыков (Skill ordering)" section and update it.

Current:
```markdown
**Быстрый старт:** `/speckit-start` — guided onboarding, объединяет init + prd + requirements в одну сессию. Рекомендуется для новых пользователей.
```

New:
```markdown
**Быстрый старт:**
- `/speckit-quick` — экспресс-режим: auto-routing по описанию задачи → scaffold → PRD с codebase-first контекстом. Для опытных пользователей.
- `/speckit-start` — guided onboarding с выбором режима (quick / profile / explicit). Рекомендуется для новых пользователей.
```

**Step 2: Update CHANGELOG.md**

Add entry to `initiatives/INIT-2026-006-smart-discovery/changelog/CHANGELOG.md`:

```markdown
## [0.1.0] — 2026-04-12

### Added
- `/speckit-quick` — auto-routing command (REQ-DISC-001, REQ-DISC-002, REQ-DISC-006)
- `.specify/memory/risk-keywords.yml` — risk-keyword dictionary
- `/speckit-start` routing choice (quick / profile / explicit)
- `/speckit-prd` codebase-first context loading (REQ-DISC-003, REQ-DISC-004)
- `/speckit-prd` depth modes — Quick/Standard/Deep (REQ-DISC-005)
```

**Step 3: Commit**

```bash
git add .specify/memory/constitution.md initiatives/INIT-2026-006-smart-discovery/changelog/CHANGELOG.md
git commit -m "docs(006): update constitution and changelog for smart discovery"
```

---

### Task 7: Update requirement status + trace

**Files:**
- Modify: `initiatives/INIT-2026-006-smart-discovery/requirements.yml`

**Step 1: Update REQ status to implemented**

For each of the 6 REQ-IDs, change `status: draft` → `status: implemented` and add trace links:

```yaml
requirements:
  - id: "REQ-DISC-001"
    status: implemented  # was: draft
    trace:
      prd: "prd.md#scope"
      tests:
        - "Manual: /speckit-quick 'fix typo' → Minimal"
      components:
        - ".claude/commands/speckit-quick.md"
        - ".specify/memory/risk-keywords.yml"

  - id: "REQ-DISC-002"
    status: implemented
    trace:
      prd: "prd.md#риски-и-ограничения"
      tests:
        - "Manual: /speckit-quick 'JWT auth' → Standard + warning"
      components:
        - ".specify/memory/risk-keywords.yml"

  - id: "REQ-DISC-003"
    status: implemented
    trace:
      prd: "prd.md#scope"
      tests:
        - "Manual: /speckit-prd with domains/notifications/glossary.md → proposed terms"
      components:
        - ".claude/commands/speckit-prd.md"

  - id: "REQ-DISC-004"
    status: implemented
    trace:
      prd: "prd.md#scope"
      tests:
        - "Manual: /speckit-prd with L2 architecture → proposed answer"
      components:
        - ".claude/commands/speckit-prd.md"

  - id: "REQ-DISC-005"
    status: implemented
    trace:
      prd: "prd.md#scope"
      tests:
        - "Manual: /speckit-prd --depth deep → 10-15 questions"
      components:
        - ".claude/commands/speckit-prd.md"

  - id: "REQ-DISC-006"
    status: implemented
    trace:
      prd: "prd.md#scope"
      tests:
        - "Manual: /speckit-quick override Minimal→Standard → enhanced scaffold"
      components:
        - ".claude/commands/speckit-quick.md"
```

**Step 2: Validate**

Run: `make validate`
Expected: PASS

**Step 3: Commit**

```bash
git add initiatives/INIT-2026-006-smart-discovery/requirements.yml
git commit -m "feat(006): update REQ status to implemented + add trace links"
```

---

### Task 8: Validate and run acceptance tests

**Files:**
- No new files — validation only

**Step 1: Run make check-all**

Run: `make check-all 2>&1 | tail -20`
Expected: No NEW errors from our changes. Pre-existing warnings are acceptable.

**Step 2: Manual acceptance test — scenario 1 (Minimal auto-detect)**

Run: `/speckit-quick "Исправить опечатку в README"`
Expected: Profile = Minimal, no risk warnings, scaffold offered.

**Step 3: Manual acceptance test — scenario 2 (Standard risk-keyword)**

Run: `/speckit-quick "Добавить JWT auth в API gateway с rate limiting"`
Expected: Profile = Standard, warning about "auth" keyword.

**Step 4: Manual acceptance test — scenario 3 (Extended GDPR)**

Run: `/speckit-quick "Обработка ПДн пользователей по 152-ФЗ"`
Expected: Profile = Extended, warning about "ПДн" keyword.

**Step 5: Final commit**

```bash
git add -A
git commit -m "feat(006): complete INIT-2026-006-smart-discovery — auto-routing + codebase-first"
```
