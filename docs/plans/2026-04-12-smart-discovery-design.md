# Design: Smart Discovery — Auto-Routing + Codebase-First Elicitation

**Initiative:** INIT-2026-006-smart-discovery
**Date:** 2026-04-12
**Author:** @dmitriy
**Approach:** B — Unified flow through `/speckit-start`

---

## Context

SpecKit requires manual profiling (8 questions) and open-ended PRD elicitation (5 questions from scratch) even for trivial tasks. 60-80% of PRD answers already exist in L1 domains, L2 architecture, and previous L3 initiatives. Competitor Datarim demonstrates auto-routing by LOC/risk and proposed-answer discovery.

**Goal:** Reduce time-to-first-validate from ~45 min to ~15 min (Minimal) and from ~2-4 hours to ~1-1.5 hours (Standard).

## Architecture

Three components integrated into a single flow:

```
User: /speckit-start or /speckit-quick
  │
  ├─ [1] "Опиши задачу в 1-2 предложениях"
  │      ↓
  │   Auto-Routing Engine (risk-keywords.yml)
  │      ↓
  │   Profile suggestion + risk warnings
  │      ↓
  │   User confirms / overrides / → /speckit-profile
  │
  ├─ [2] /speckit-init (scaffold by determined profile)
  │
  └─ [3] /speckit-prd (with codebase-first context)
         ├─ depth mode = f(profile)
         ├─ before each Q → scan L1/L2/L3 artifacts
         └─ proposed answer with source + staleness warning
```

### Files to create

| File | Purpose |
|------|---------|
| `.claude/commands/speckit-quick.md` | Standalone shortcut — delegates to start --quick flow |
| `.specify/memory/risk-keywords.yml` | Risk-keyword dictionary (single source of truth for auto-routing) |

### Files to modify

| File | Change |
|------|--------|
| `.claude/commands/speckit-start.md` | Add Step 0 routing choice (quick / profile / explicit) |
| `.claude/commands/speckit-prd.md` | Add context loading + depth modes + proposed answers |

---

## Component 1: Auto-Routing Engine

**REQ-IDs:** REQ-DISC-001, REQ-DISC-002, REQ-DISC-006

### risk-keywords.yml

```yaml
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
```

### Routing Algorithm

```
INPUT: description (1-2 sentences from user)

STEP 1: Risk-keyword scan
  matched_high = [kw for kw in high_risk if regex_match(kw.pattern, description)]
  matched_medium = [kw for kw in medium_risk if regex_match(kw.pattern, description)]
  
  if matched_high:
    profile = max(kw.min_profile for kw in matched_high)
  elif len(matched_medium) >= 3:
    profile = "standard"
  else:
    profile = "minimal"

STEP 2: Component count estimation
  component_mentions = count_mentions(description, ["файл", "компонент", "сервис", 
    "endpoint", "таблица", "модуль", "контракт"])
  if component_mentions > 15: profile = max(profile, "extended")
  elif component_mentions > 5: profile = max(profile, "standard")

STEP 3: Output
  if profile == "minimal" and no matched_high:
    → scaffold immediately, skip /speckit-profile
  else:
    → show: "Предложен профиль: {profile}."
    → if matched_high: show risk warnings with reasons
    → prompt: "Подтвердить? [Да / Переопределить / Пройти /speckit-profile]"
```

### Profile Override (REQ-DISC-006)

- **Override UP** (Minimal → Standard): scaffold enhanced with Standard artifacts (design.md, contracts/, ops/)
- **Override DOWN** (Standard → Minimal): warning about risk-keywords found + user confirms

---

## Component 2: Codebase-First Context Loading

**REQ-IDs:** REQ-DISC-003, REQ-DISC-004

### Question → File Mapping

| PRD Question | Files to check | Section to extract |
|---|---|---|
| Проблема / Цель | Last 3 L3 `initiatives/*/prd.md` | "Цель и ожидаемый эффект" |
| Tech stack / Архитектура | L2 `products/{product}/architecture/overview.md` | Technology, Stack, Components |
| NFR targets | L2 `products/{product}/nfr-baseline/baseline.md` | All |
| Терминология | L1 `domains/*/glossary.md` (matching domain) | All |
| API patterns | Last 3 L3 `initiatives/*/contracts/openapi.yaml` | paths section |
| Пользователи / Сценарии | Last 3 L3 `initiatives/*/prd.md` | "Пользователи и сценарии" |
| Security | L3 `initiatives/*/ops/threat-model.md` (if Extended) | Threats, Mitigations |
| Compliance | L1 `domains/*/regulatory/` | All |

### Context Loading Logic

```
BEFORE each PRD question:

1. Determine question domain from mapping table
2. Glob for matching files (max 3, sorted by last_updated desc)
3. Read matched files, extract heading-matched sections
4. If relevant context found:
   → Generate proposed answer:
     "Предположительно: {answer}
      (источник: {relative_path}, обновлён {date})
      Верно? [Да / Нет / Уточнить]"
   → If source.last_updated > 90 days:
     append "⚠️ Источник обновлён > 90 дней назад"
5. If no relevant context found:
   → Ask as open-ended question (current behavior, no change)
```

### Constraints

- Max 3 files per question (prevents context overflow)
- Skip archived initiatives (initiative_status == "archived")
- No semantic search — file path conventions only (predictable, offline, no dependencies)
- Graceful degradation: no artifacts → no proposed answer → open-ended question

---

## Component 3: Discovery Depth Modes

**REQ-ID:** REQ-DISC-005

| Mode | Questions | Trigger | Topics |
|---|---|---|---|
| Quick | 3-5 | profile = minimal | Problem, Scope, REQs, Risks (opt), Metrics (opt) |
| Standard | 5-10 | profile = standard | Quick + Users, Architecture, Contracts, NFR, Dependencies |
| Deep | 10-15 | profile = extended+ | Standard + Security, Compliance, Migration, Rollout, Cross-initiative |

Override: `--depth quick|standard|deep` flag on `/speckit-prd`.

---

## Component 4: /speckit-start Modification

Current flow (5 questions, always Minimal) gets a new Step 0:

```
NEW STEP 0: "Как хочешь начать?"
  a) "Опиши задачу в 1-2 предложениях" → auto-routing → profile
  b) "Пройти risk assessment" → /speckit-profile (current full flow)
  c) "Я знаю профиль: <minimal|standard|...>" → skip routing

→ then current flow (slug, problem, outcome, scope, product)
  but PRD step uses codebase-first context loading
```

### /speckit-quick

Standalone shortcut that runs the same flow as option (a) above:
1. Ask for description
2. Run auto-routing
3. Delegate to `/speckit-start` with determined profile

---

## Integration with Constitution

- Follows "Порядок навыков": quick → init → prd → requirements
- risk-keywords.yml is a new canonical file in `.specify/memory/`
- Profile decision tree in speckit-profile.md remains authoritative for full risk assessment
- Auto-routing is a heuristic shortcut — always offers escape to full /speckit-profile

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Over-classification: "API" in 80% of descriptions | Always suggests Standard | medium_risk requires ≥3 matches, not 1 |
| Under-classification: high-risk without keywords | Missed risk → wrong profile | Always offer "Переопределить / /speckit-profile" |
| Context staleness: L2 overview.md outdated | Wrong proposed answer | Timestamp warning > 90 days |
| False confidence: user auto-confirms | PRD quality drops | Show source + date, require explicit [Да/Нет/Уточнить] |
| Context overload: many L3 initiatives | Slow glob, noisy proposals | Max 3 files per question, sorted by date |

---

## Acceptance Criteria (from requirements.yml)

1. Input: "Исправить опечатку в README" → Profile = Minimal, scaffold created, 0 questions
2. Input: "Добавить JWT auth в API gateway" → Propose Standard, warning "auth, API"
3. Input: "Обработка ПДн пользователей по 152-ФЗ" → Propose Extended, warning "ПДн"
4. Given `domains/notifications/glossary.md` exists → terms proposed in PRD context
5. Given `products/platform/architecture/overview.md` mentions PostgreSQL → proposed as storage answer
6. Given no relevant L1/L2/L3 context → open-ended question (no proposed answer)
7. Given profile = Minimal → 3-5 PRD questions (Quick mode)
8. Given `--depth deep` flag → 10-15 questions regardless of profile

---

## Effort Estimate

| Component | Files | Effort |
|---|---|---|
| risk-keywords.yml | 1 new | 1 hr |
| speckit-quick.md | 1 new | 2 hrs |
| speckit-start.md modification | 1 mod | 2 hrs |
| speckit-prd.md modification (context loading + depth) | 1 mod | 4 hrs |
| Testing (8 scenarios) | — | 2 hrs |
| Docs (QUICKSTART.md, constitution.md) | 2 mod | 1 hr |
| **Total** | **6 files** | **~12 hrs** |
