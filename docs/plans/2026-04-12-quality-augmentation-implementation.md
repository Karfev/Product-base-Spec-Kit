# Quality Augmentation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add multi-perspective ADR review (`/speckit-consilium`) and codified AI quality constraints (Five Pillars + enforcement) to SpecKit.

**Architecture:** Sequential execution: Phase 1 creates consilium (new YAML config + command), Phase 2 adds quality gates (new markdown doc + speckit-implement modification + CI extension). Both target Standard+ profile. Phase 3 updates REQ status and validates.

**Tech Stack:** Claude Code skills (.md command files), YAML config, Python (check-spec-quality.py), Makefile targets.

**Design doc:** `docs/plans/2026-04-12-quality-augmentation-design.md`

**Initiative:** INIT-2026-007-quality-augmentation  
**L4 Specs:** 008-consilium, 010-ai-quality-gates

---

## Phase 1: Consilium (Spec 008)

### Task 1: Create consilium-roles.yml

**Files:**
- Create: `.specify/memory/consilium-roles.yml`

**Step 1: Create the roles config file**

```yaml
# Consilium role definitions for multi-perspective ADR review.
# Used by /speckit-consilium to compose review panels.
# Canonical source of truth for domain review roles (REQ-QUAL-002).

roles:
  - name: "Прикладная архитектура"
    id: "arch"
    description: "Оценка архитектурных решений, соответствие C4/arc42, backward compatibility"
    context_files:
      - "products/{product}/architecture/overview.md"
      - "domains/{domain}/canonical-model.md"
    checklist:
      - "Решение соответствует C4 context/containers?"
      - "Нет архитектурных anti-patterns (God service, distributed monolith)?"
      - "Backward compatibility сохранена?"
      - "Альтернативы рассмотрены с trade-offs?"

  - name: "ИБ (Information Security)"
    id: "security"
    description: "Анализ безопасности: auth model, PII, input validation, secrets management"
    context_files:
      - "ops/threat-model.md"
      - "domains/{domain}/nfr.md"
    checklist:
      - "Auth model определён и адекватен?"
      - "PII/ПДн обработка соответствует 152-ФЗ?"
      - "Input validation на всех boundaries?"
      - "Secrets management определён?"

  - name: "БД/нагрузки"
    id: "db-load"
    description: "Оценка схемы данных, миграций, индексов, нагрузочного профиля"
    context_files:
      - "products/{product}/nfr-baseline/baseline.md"
      - "ops/slo.yaml"
    checklist:
      - "Схема данных нормализована / обоснована денормализация?"
      - "Миграция backward-compatible?"
      - "Индексы для hot paths определены?"
      - "Нагрузочный профиль оценён (RPS, P95 latency)?"

  - name: "Инфраструктура"
    id: "infra"
    description: "Deployment topology, rollback, scaling, мониторинг"
    context_files:
      - "delivery/rollout.md"
      - "ops/prr-checklist.md"
    checklist:
      - "Deployment topology определена?"
      - "Rollback strategy описана?"
      - "Горизонтальное масштабирование возможно?"
      - "Мониторинг и alerting настроены?"

  - name: "Интеграции"
    id: "integrations"
    description: "Contract compatibility, breaking changes, event schema versioning, retry/DLQ"
    context_files:
      - "contracts/openapi.yaml"
      - "contracts/asyncapi.yaml"
      - "domains/{domain}/event-catalog.md"
    checklist:
      - "Contract changes backward-compatible?"
      - "Breaking changes задокументированы с deprecation plan?"
      - "Event schema versioning определён?"
      - "Retry/DLQ strategy для async определена?"

# Presets map to Архкомм governance levels.
presets:
  standard:
    description: "Default for Standard profile (У0→У1 light)"
    roles: ["arch", "security", "infra"]

  archkom-l1:
    description: "Default for Extended profile (У1 full Архкомм)"
    roles: ["arch", "security", "db-load", "infra", "integrations"]

  archkom-l2:
    description: "Default for Enterprise profile (У2 full Архкомм + extended domains)"
    roles: ["arch", "security", "db-load", "infra", "integrations"]
    # Note: archkom-l2 can be extended with additional roles (TCO, QA, CI/CD)
    # via --roles flag. Base set is same as archkom-l1 in v1.

# Profile-to-preset mapping (used when no --preset or --roles specified).
profile_defaults:
  minimal: null  # Consilium not applicable to Minimal profile
  standard: "standard"
  extended: "archkom-l1"
  enterprise: "archkom-l2"
```

**Step 2: Validate YAML syntax**

Run: `python3 -c "import yaml; yaml.safe_load(open('.specify/memory/consilium-roles.yml'))"`
Expected: No output (valid YAML)

**Step 3: Commit**

```bash
git add .specify/memory/consilium-roles.yml
git commit -m "feat(008-consilium): T1 — create consilium-roles.yml with 5 roles + 3 presets (REQ-QUAL-002)"
```

---

### Task 2: Define acceptance tests for consilium

**Files:**
- Reference: `products/platform/decisions/PLAT-0003-async-queue.md` (PoC ADR)
- Reference: `.specify/specs/008-consilium/spec.md` (acceptance criteria)

**Step 1: Document test scenarios**

No code to write — these are manual test scenarios for PoC validation in Task 4. Record them here for traceability:

**Scenario 1 — Standard preset on PLAT-0003:**
- Input: `/speckit-consilium products/platform/decisions/PLAT-0003-async-queue.md`
- Expected: 3 roles (arch, security, infra) generate reviews. Output contains "Доменные оценки" table with verdict per role.

**Scenario 2 — Custom roles:**
- Input: `/speckit-consilium products/platform/decisions/PLAT-0003-async-queue.md --roles "security,integrations"`
- Expected: Only 2 roles participate. Other roles excluded.

**Scenario 3 — Блокер detection:**
- Input: ADR without rollback strategy reviewed by "infra" role
- Expected: Infra role outputs "Блокер" verdict. Overall status = "требует доработки".

**Scenario 4 — Re-run idempotency:**
- Input: Run consilium twice on same ADR
- Expected: "Доменные оценки" section replaced (not duplicated).

**Step 2: Commit**

No file changes — scenarios are documented in this plan. Proceed to Task 3.

---

### Task 3: Create speckit-consilium.md command

**Files:**
- Create: `.claude/commands/speckit-consilium.md`

**Step 1: Create the command file**

```markdown
---
description: Multi-perspective ADR review — generate domain evaluations from Архкомм-aligned roles
argument-hint: <path-to-ADR> [--preset standard|archkom-l1|archkom-l2] [--roles "role1,role2"]
---

You are running a structured multi-perspective review of an ADR (Architecture Decision Record).

## Your job

1. **Parse arguments.**
   - `$ARGUMENTS` contains: `<adr_path>` and optional flags `--preset <name>` or `--roles "<comma-separated>"`.
   - If no ADR path provided, ask: "Укажи путь к ADR файлу (e.g., products/platform/decisions/PLAT-0003-async-queue.md)"

2. **Read the ADR file.** Parse its content completely.

3. **Read role definitions.**
   Read `.specify/memory/consilium-roles.yml` — load `roles`, `presets`, and `profile_defaults`.

4. **Determine panel composition (REQ-QUAL-002, REQ-QUAL-006):**

   **Priority order:**
   a. If `--roles` flag provided → parse comma-separated role IDs, match against `roles[].id` in consilium-roles.yml. Error if any ID not found.
   b. If `--preset` flag provided → load preset from `presets` section. Error if preset not found.
   c. If neither flag → auto-detect from initiative profile:
      - Read the initiative's `requirements.yml` metadata to get `profile`
      - Map profile to preset using `profile_defaults` in consilium-roles.yml
      - If profile = `minimal` or mapping is `null` → inform user: "Consilium не применяется к Minimal профилю. Используйте `--preset standard` для принудительного запуска." Stop.

   Announce: "Panel: {N} ролей ({role names}). Preset: {preset_name|custom}."

5. **Execute sequential role reviews (REQ-QUAL-001).**

   For each role in the panel:

   a. **Load context files.** For each path in `role.context_files`:
      - Replace `{product}` with the product from initiative metadata (or ask user)
      - Replace `{domain}` with the domain from initiative metadata (or infer from ADR path)
      - If the file exists → read it (extract relevant sections, max 500 tokens per file)
      - If the file doesn't exist → note: "Артефакт {path} не найден — пропускаем этот контекст"

   b. **Analyze the ADR** from this role's perspective using the checklist:

      For each checklist item:
      1. Check if the item is covered in the ADR
      2. If covered adequately → **OK** with brief confirmation
      3. If covered but with concerns → **Замечание** with specific observation and artifact reference
      4. If critical gap → **Блокер** with specific description of what's missing

   c. **Generate role output** in this format:
      ```
      ### {role.name}

      | Пункт | Статус | Комментарий |
      |---|---|---|
      | {checklist_item_1} | OK / Замечание / Блокер | {specific detail with artifact reference} |
      | {checklist_item_2} | ... | ... |

      **Итог:** {OK / Замечание / Блокер} — {one-sentence summary}
      ```

6. **Aggregate results (REQ-QUAL-003).**

   Build the "Доменные оценки" section:

   ```markdown
   ## Доменные оценки (consilium)

   > Сгенерировано `/speckit-consilium` {today's date}. Preset: {preset_name}.

   | Домен | Статус | Комментарий |
   |---|---|---|
   | {role_1.name} | {verdict} | {summary} |
   | {role_2.name} | {verdict} | {summary} |
   | ... | ... | ... |

   **Итог:** {overall_verdict}
   ```

   Overall verdict logic:
   - Any **Блокер** → "Требует доработки"
   - Only **Замечания** (no Блокеры) → "Одобрено с условиями"
   - All **OK** → "Одобрено"

   If overall = "Требует доработки" or "Одобрено с условиями", add conditions table:
   ```markdown
   **Условия:**

   | # | Условие | Источник | Приоритет |
   |---|---------|----------|-----------|
   | 1 | {specific action required} | {role_name} | Блокер / Замечание |
   ```

7. **Inject section into ADR.**

   - Check if ADR already has a `## Доменные оценки` section
   - If yes → **replace** the existing section (from `## Доменные оценки` to the next `## ` heading or end of file)
   - If no → **append** the section before the last heading or at the end of the file

8. **Print summary to console.**

   ```
   Consilium review complete for {adr_filename}

   Panel: {N} roles ({preset_name})
   | Домен | Статус |
   |---|---|
   | {role_name} | {verdict} |

   Overall: {overall_verdict}
   {If blockers: "Blockers: N — resolve before Архкомм submission"}
   ```

## Rules
- NEVER auto-approve — consilium generates review, human decides
- Each role MUST reference specific artifacts or ADR sections in findings — no vague "looks good"
- If context file doesn't exist, role still runs but notes the missing context
- Checklist items without clear evidence in ADR → default to "Замечание" (not OK)
- For Standard+ profile only — Minimal initiatives skip consilium
- Maximum context per role: 500 tokens per file, 3 files max (prevent context overflow)
- Output format MUST be compatible with ADR-template-v2 "Доменные оценки" section
```

**Step 2: Verify file created correctly**

Run: `head -5 .claude/commands/speckit-consilium.md`
Expected: Shows frontmatter with description and argument-hint.

**Step 3: Commit**

```bash
git add .claude/commands/speckit-consilium.md
git commit -m "feat(008-consilium): T2b — create /speckit-consilium command (REQ-QUAL-001, REQ-QUAL-003, REQ-QUAL-006)"
```

---

### Task 4: PoC validation on PLAT-0003

**Files:**
- Modify: `products/platform/decisions/PLAT-0003-async-queue.md` (consilium will inject section)

**Step 1: Run consilium on PLAT-0003**

Run: `/speckit-consilium products/platform/decisions/PLAT-0003-async-queue.md --preset standard`

Expected:
- 3 roles execute (arch, security, infra)
- "Доменные оценки" section injected into PLAT-0003-async-queue.md
- Console summary shows verdicts per role

**Step 2: Verify output format**

Read `products/platform/decisions/PLAT-0003-async-queue.md` and confirm:
- `## Доменные оценки (consilium)` section exists
- Table has 3 rows (one per role)
- Each row has Домен, Статус, Комментарий columns
- Overall verdict is present

**Step 3: Verify re-run idempotency**

Run consilium again on the same file.
Verify: "Доменные оценки" section replaced, not duplicated.

**Step 4: Commit**

```bash
git add products/platform/decisions/PLAT-0003-async-queue.md
git commit -m "feat(008-consilium): T3 — PoC validation on PLAT-0003 (REQ-QUAL-001)"
```

---

### Task 5: Update 008-consilium tasks.md

**Files:**
- Modify: `.specify/specs/008-consilium/tasks.md`

**Step 1: Mark completed tasks**

Mark T1, T2a, T2b, T3 as done in `.specify/specs/008-consilium/tasks.md`:

```markdown
- [x] **T1:** Создать `.specify/memory/consilium-roles.yml` ...
- [x] **T2a:** Определить acceptance tests ...
- [x] **T2b:** Создать `.claude/commands/speckit-consilium.md` ...
- [x] **T3:** PoC validation ...
- [x] **T4:** Документация ...
- [x] **T5:** Обновить `CHANGELOG.md` инициативы
```

**Step 2: Commit**

```bash
git add .specify/specs/008-consilium/tasks.md
git commit -m "feat(008-consilium): T4+T5 — mark tasks complete, update docs"
```

---

## Phase 2: AI Quality Gates (Spec 010)

### Task 6: Create ai-quality-gates.md

**Files:**
- Create: `tools/ai-quality-gates.md`

**Step 1: Create the quality gates document**

```markdown
# AI Quality Gates — Five Pillars (SpecKit Edition)

> Кодифицированные ограничения качества для implementation phase.
> Применяется: Standard+ профиль, фазы T2a/T2b в tasks.md.
> REQ-QUAL-004.

---

## Когда применять

- **Standard, Extended, Enterprise** профили — обязательно
- **Minimal** — не применяется (quick fix, overhead не оправдан)
- **Фаза:** T2a (написание тестов) и T2b (реализация) в `/speckit-implement`

---

## Pillar 1: Decomposition (Декомпозиция)

**Правила:**
- Max **50 LOC** per method/function (excluding comments and blank lines)
- Max **7-9 объектов/сущностей** в активном scope per task
- **Single Responsibility:** одна функция = одна задача
- Если метод > 50 LOC → декомпозировать до продолжения

**Пример (хорошо):**
```python
def validate_request(req):
    """Validate incoming request. 12 LOC."""
    check_auth(req.headers)
    check_schema(req.body)
    check_rate_limit(req.client_id)

def check_auth(headers):
    """Verify auth token. 8 LOC."""
    ...
```

**Anti-pattern:**
```python
def handle_request(req):
    """Everything in one method. 200+ LOC."""
    # auth check...
    # schema validation...
    # rate limit...
    # business logic...
    # response formatting...
    # error handling...
```

**Enforcement:** `/speckit-implement` проверяет: "Метод {name} = {N} строк. Decompose?"

---

## Pillar 2: Test-First (TDD)

**Правила:**
- **T2a MUST complete before T2b** starts
- Тесты определяют интерфейс: write test → derive function signature → implement
- **Arrange-Act-Assert** pattern для unit tests
- Contract tests валидируют OpenAPI/AsyncAPI compliance

**Пример (хорошо):**
```python
# T2a: Write failing test FIRST
def test_create_api_key_returns_201():
    response = client.post("/api-keys", json={"name": "test"})
    assert response.status_code == 201
    assert "id" in response.json()

# T2b: THEN implement to make it pass
@app.post("/api-keys")
def create_api_key(req: CreateKeyRequest):
    key = service.create(req.name)
    return {"id": key.id}, 201
```

**Anti-pattern:**
- Написать реализацию, потом подогнать тесты
- Тесты без assertions (test that passes by default)
- T2b без T2a → CI warning

**Enforcement:**
- `/speckit-implement` блокирует T2b если T2a не marked done
- `check-spec-quality.py`: T2b `[x]` before T2a `[x]` → CI warning

---

## Pillar 3: Architecture-First (Архитектура в первую очередь)

**Правила:**
- Создать **skeleton stubs** (interfaces, type signatures, empty handlers) до реализации
- Stubs **MUST match contract signatures** (OpenAPI paths, AsyncAPI handlers)
- Реализовать **один метод за раз**, не целый модуль

**Пример (хорошо):**
```python
# Step 1: Stub matching OpenAPI contract
@app.post("/api-keys")
def create_api_key(req: CreateKeyRequest) -> CreateKeyResponse:
    raise NotImplementedError  # stub

@app.delete("/api-keys/{key_id}")
def delete_api_key(key_id: str) -> None:
    raise NotImplementedError  # stub

# Step 2: Implement one at a time
@app.post("/api-keys")
def create_api_key(req: CreateKeyRequest) -> CreateKeyResponse:
    key = service.create(req.name)
    return CreateKeyResponse(id=key.id, created_at=key.created_at)
```

**Anti-pattern:**
- Реализовать всю бизнес-логику без skeleton stubs
- Stubs с другими signatures чем в OpenAPI

**Enforcement:** `/speckit-implement` спрашивает: "Stubs created and match contracts? [Y/N]"

---

## Pillar 4: Focused Work (Фокусированная работа)

**Правила:**
- **One task = one bounded context** (single handler, single endpoint, single event)
- Explicit scope boundaries перед каждым T2b: "This task covers: {files}, {methods}"
- **No side-effect changes** outside declared scope

**Пример (хорошо):**
```
Scope for T2b: 
- File: src/handlers/api_keys.py
- Methods: create_api_key()
- Contract: POST /api-keys (openapi.yaml)
```

**Anti-pattern:**
- "While I'm here, let me also refactor the auth module"
- Touching 10 files in one task
- No declared scope → changes leak everywhere

**Enforcement:** `/speckit-implement` prompts: "Scope for this task: {declared scope}. Proceed? [Y/N]"

---

## Pillar 5: Contract-Aware (Контрактная осведомлённость)

> Специфика SpecKit — differentiator vs generic AI quality frameworks.

**Правила:**
- Implementation **MUST match contract signatures:**
  - REST: HTTP method + path + request/response schemas from OpenAPI
  - Events: channel + message schema from AsyncAPI
  - Data: entity schemas from `contracts/schemas/*.json`
- **`make lint-contracts` MUST pass** before T2b
- Breaking changes: require ADR + deprecation plan

**Пример (хорошо):**
```yaml
# openapi.yaml defines:
paths:
  /api-keys:
    post:
      requestBody:
        schema: { $ref: '#/components/schemas/CreateKeyRequest' }
      responses:
        201:
          schema: { $ref: '#/components/schemas/CreateKeyResponse' }
```
```python
# Implementation matches contract exactly:
@app.post("/api-keys", status_code=201)
def create_api_key(req: CreateKeyRequest) -> CreateKeyResponse:
    ...
```

**Anti-pattern:**
- Endpoint returns 200 instead of 201 (contract says 201)
- Request body has different field names than schema
- Missing contract for new endpoint

**Enforcement:**
- `/speckit-implement` runs `make lint-contracts` before T2b
- Mismatch → blocker with specific diff

---

## Pre-flight Checklist (для /speckit-implement)

Before starting T2b, verify:

- [ ] T2a tests written and failing (RED)?
- [ ] Architecture stubs created?
- [ ] Stubs match contracts (`make lint-contracts`)?
- [ ] Scope declared (which files, which methods)?
- [ ] Quality gates document read?

If any item unchecked → WARNING with specific blocker.
If all checked → proceed to implementation.
```

**Step 2: Verify file**

Run: `head -5 tools/ai-quality-gates.md`
Expected: Shows title and description.

**Step 3: Commit**

```bash
git add tools/ai-quality-gates.md
git commit -m "feat(010-ai-quality-gates): T1 — create ai-quality-gates.md with Five Pillars (REQ-QUAL-004)"
```

---

### Task 7: Modify speckit-implement.md — add pre-flight checklist

**Files:**
- Modify: `.claude/commands/speckit-implement.md:12-18`

**Step 1: Add pre-flight checklist before T2b**

In `.claude/commands/speckit-implement.md`, find the section after line 12 (`- For T2b: run tests and confirm they PASS (GREEN)`) and add the quality gates pre-flight. The modification inserts a new section between the current job description (step 3) and the GSD-aware mode section.

Replace:

```markdown
3. Implement ONLY that one task:
   - Run the relevant validation after completing the task
   - For T2a: run tests and confirm they FAIL (RED)
   - For T2b: run tests and confirm they PASS (GREEN)
   - Mark the task complete `[x]`
   - Commit: `git commit -m "feat($ARGUMENTS): complete T<N> — <brief description>"`
4. Report what was done and stop — wait for user to continue to the next task
```

With:

```markdown
3. Implement ONLY that one task:
   - Run the relevant validation after completing the task
   - For T2a: run tests and confirm they FAIL (RED)
   - **For T2b (Standard+ profile only) — run pre-flight checklist first (REQ-QUAL-005):**
     1. Read `tools/ai-quality-gates.md` — load Five Pillars
     2. Read the initiative's `requirements.yml` to check profile
     3. If profile is `standard`, `extended`, or `enterprise`:
        - Verify T2a is marked `[x]` in tasks.md. If not → STOP: "T2a incomplete — write tests first (Pillar 2: Test-First)"
        - Ask: "Architecture stubs created and match contracts? [Y/N]" (Pillar 3)
        - If contracts exist: run `make lint-contracts`. If fail → STOP with specific diff (Pillar 5)
        - Ask: "Scope for this task: {files, methods}. Confirmed? [Y/N]" (Pillar 4)
        - If any check fails → show WARNING with specific blocker from quality gates
        - If all pass → proceed to implementation
     4. If profile is `minimal` → skip pre-flight, proceed directly
   - For T2b: run tests and confirm they PASS (GREEN)
   - After T2b: if method > 50 LOC, suggest decomposition (Pillar 1)
   - Mark the task complete `[x]`
   - Commit: `git commit -m "feat($ARGUMENTS): complete T<N> — <brief description>"`
4. Report what was done and stop — wait for user to continue to the next task
```

**Step 2: Verify the edit**

Run: `grep -n "pre-flight" .claude/commands/speckit-implement.md`
Expected: Shows the new pre-flight section.

**Step 3: Commit**

```bash
git add .claude/commands/speckit-implement.md
git commit -m "feat(010-ai-quality-gates): T2b — add pre-flight checklist to /speckit-implement (REQ-QUAL-005)"
```

---

### Task 8: Extend check-spec-quality.py — add task ordering check

**Files:**
- Modify: `tools/scripts/check-spec-quality.py:218-231`

**Step 1: Add check_task_ordering function**

In `tools/scripts/check-spec-quality.py`, replace the current T2a/T2b check (lines 218-231) with an enhanced version that also detects T2b checked without T2a checked:

Replace the block starting at line 218 (`# 5) RED -> GREEN sequence in tasks.md: T2a before T2b.`):

```python
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
```

With:

```python
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
```

**Step 2: Verify the change**

Run: `make check-spec-quality 2>&1 | tail -10`
Expected: No new errors from our changes. Existing specs should still pass.

**Step 3: Commit**

```bash
git add tools/scripts/check-spec-quality.py
git commit -m "feat(010-ai-quality-gates): T3 — add T2b-before-T2a detection to check-spec-quality.py (REQ-QUAL-005)"
```

---

### Task 9: Update 010-ai-quality-gates tasks.md

**Files:**
- Modify: `.specify/specs/010-ai-quality-gates/tasks.md`

**Step 1: Mark completed tasks**

Mark all tasks as done in `.specify/specs/010-ai-quality-gates/tasks.md`:

```markdown
- [x] **T1:** Создать `tools/ai-quality-gates.md` ...
- [x] **T2a:** Определить acceptance tests ...
- [x] **T2b:** Модифицировать `.claude/commands/speckit-implement.md` ...
- [x] **T3:** Расширить `tools/scripts/check-spec-quality.py` ...
- [x] **T4:** Тестирование ...
- [x] **T5:** Обновить `CHANGELOG.md` инициативы
```

**Step 2: Commit**

```bash
git add .specify/specs/010-ai-quality-gates/tasks.md
git commit -m "feat(010-ai-quality-gates): T4+T5 — mark tasks complete"
```

---

## Phase 3: Closure

### Task 10: Update requirements.yml — status + trace links

**Files:**
- Modify: `initiatives/INIT-2026-007-quality-augmentation/requirements.yml`

**Step 1: Update all 6 REQ-IDs**

Change `status: draft` → `status: implemented` for all 6 requirements. Add trace links with component paths:

For each requirement, add/update the `trace:` block:

- **REQ-QUAL-001** → components: `.claude/commands/speckit-consilium.md`
- **REQ-QUAL-002** → components: `.specify/memory/consilium-roles.yml`
- **REQ-QUAL-003** → components: `.claude/commands/speckit-consilium.md` (output format section)
- **REQ-QUAL-004** → components: `tools/ai-quality-gates.md`
- **REQ-QUAL-005** → components: `.claude/commands/speckit-implement.md`, `tools/scripts/check-spec-quality.py`
- **REQ-QUAL-006** → components: `.claude/commands/speckit-consilium.md`, `.specify/memory/consilium-roles.yml`

Also update `metadata.version` to `"0.2.0"` and `metadata.last_updated` to today.

**Step 2: Validate**

Run: `make validate`
Expected: PASS

**Step 3: Commit**

```bash
git add initiatives/INIT-2026-007-quality-augmentation/requirements.yml
git commit -m "feat(007): update REQ status to implemented + add trace links"
```

---

### Task 11: Update CHANGELOG.md + final validation

**Files:**
- Modify: `initiatives/INIT-2026-007-quality-augmentation/changelog/CHANGELOG.md`

**Step 1: Add v0.2.0 entry to CHANGELOG**

Prepend before the existing `## [0.1.0]` entry:

```markdown
## [0.2.0] - 2026-04-12

### Added

- `/speckit-consilium` — multi-perspective ADR review command (REQ-QUAL-001, REQ-QUAL-003)
- `.specify/memory/consilium-roles.yml` — 5 domain roles + 3 Архкомм presets (REQ-QUAL-002, REQ-QUAL-006)
- `tools/ai-quality-gates.md` — Five Pillars of AI Quality (REQ-QUAL-004)

### Changed

- `/speckit-implement` — added pre-flight checklist before T2b (REQ-QUAL-005)
- `check-spec-quality.py` — added T2b-before-T2a ordering detection (REQ-QUAL-005)
- All 6 REQ-IDs status: draft → implemented
```

**Step 2: Run make check-all**

Run: `make check-all 2>&1 | tail -20`
Expected: No NEW errors from our changes. Pre-existing warnings acceptable.

**Step 3: Commit**

```bash
git add initiatives/INIT-2026-007-quality-augmentation/changelog/CHANGELOG.md
git commit -m "docs(007): update CHANGELOG for quality augmentation v0.2.0"
```

---

## Summary

| Task | Phase | Files | REQ-IDs |
|---|---|---|---|
| 1. Create consilium-roles.yml | 1 | CREATE `.specify/memory/consilium-roles.yml` | REQ-QUAL-002 |
| 2. Define acceptance tests | 1 | (documented in plan) | REQ-QUAL-001 |
| 3. Create speckit-consilium.md | 1 | CREATE `.claude/commands/speckit-consilium.md` | REQ-QUAL-001, 003, 006 |
| 4. PoC on PLAT-0003 | 1 | MODIFY `products/platform/decisions/PLAT-0003-async-queue.md` | REQ-QUAL-001 |
| 5. Update 008 tasks.md | 1 | MODIFY `.specify/specs/008-consilium/tasks.md` | — |
| 6. Create ai-quality-gates.md | 2 | CREATE `tools/ai-quality-gates.md` | REQ-QUAL-004 |
| 7. Modify speckit-implement.md | 2 | MODIFY `.claude/commands/speckit-implement.md` | REQ-QUAL-005 |
| 8. Extend check-spec-quality.py | 2 | MODIFY `tools/scripts/check-spec-quality.py` | REQ-QUAL-005 |
| 9. Update 010 tasks.md | 2 | MODIFY `.specify/specs/010-ai-quality-gates/tasks.md` | — |
| 10. Update requirements.yml | 3 | MODIFY `initiatives/INIT-2026-007-.../requirements.yml` | All 6 |
| 11. Update CHANGELOG + validate | 3 | MODIFY `initiatives/INIT-2026-007-.../changelog/CHANGELOG.md` | — |
