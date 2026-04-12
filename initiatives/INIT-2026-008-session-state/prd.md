# PRD: Session State Management

**Initiative:** INIT-2026-008-session-state
**Owner (PM):** @dmitriy
**Last updated:** 2026-04-12
**Profile:** Minimal
**Source:** Datarim competitive analysis (`CLAUDE OUTPUTS/SpecKit/SpecKit_Datarim-Analysis_Report_v1.md`)

---

## Цель и ожидаемый эффект

- **Проблема:** SpecKit не сохраняет контекст между сессиями агента. Каждый вызов `/speckit-*` начинается с нуля: агент перечитывает constitution (270 строк), requirements.yml, contracts, предыдущие L4 specs. Для длинных инициатив (Standard+, 10+ commands за lifecycle) это приводит к: (1) повторной загрузке ~2-5K tokens context на каждый command, (2) потере решений, принятых внутри сессии, (3) невозможности seamless resume после обрыва сессии.
- **Почему сейчас:** С ростом adoption (INIT-2026-004, SLO time-to-first-validate ≤ 30 мин) и появлением codebase-first discovery (INIT-2026-006) объём контекста на инициативу растёт. INIT-2026-007 добавляет consilium и quality gates — ещё больше промежуточных артефактов. Без session state пользователь теряет 5-15 мин на re-orientation при каждом возвращении к инициативе. Datarim решает это через `datarim/` directory с activeContext.md + progress.md.
- **Цель (Outcome):** Обеспечить seamless resume для длинных инициатив. Сократить время re-orientation при возвращении к инициативе с ~10 мин до ~1 мин.

## Пользователи и сценарии

- **Primary persona:** SpecKit user (architect / tech lead), работающий над Standard+ инициативой в нескольких сессиях.
- **Top JTBD / сценарии:**
  1. **Session save:** Пользователь завершает `/speckit-plan` → session state автоматически обновляется: last command, next step, decisions (REQ-SESS-001, REQ-SESS-002).
  2. **Session resume:** Пользователь открывает новую сессию → `/speckit-continue` → агент читает session state → предлагает next step (REQ-SESS-003, REQ-SESS-004).
  3. **Multi-initiative context:** Пользователь переключается между INIT → session state per initiative → dashboard (REQ-SESS-005).

## Метрики успеха

| Метрика | Baseline | Target | Период | Источник |
|---|---:|---:|---|---|
| Re-orientation time (resume initiative) | ~10 мин | ≤ 1 мин | 30d | Manual timing |
| Context re-reads per session | ~3-5 file reads | ≤ 1 (session state) | 30d | Command telemetry |
| Decisions lost between sessions | ~30% (est.) | < 5% | 90d | Retrospective |

## Scope

**In-scope:**
- Новая директория `.specify/session/` с файлами session state per initiative
- Middleware pattern: каждый `/speckit-*` command обновляет session state после выполнения
- Новый command `/speckit-continue` — resume с последнего checkpoint
- Selective context loading: вместо полного re-read constitution → load session delta

**Non-goals:**
- Real-time collaboration (multi-user session state)
- Git-tracked session state (ephemeral, `.gitignore`)
- Undo/rollback session decisions
- Модификация constitution.md или JSON schemas

## Риски и ограничения

- **Stale session:** Артефакты изменены вне pipeline → session рассинхронизирован → mitigated by mtime comparison + warning
- **Session bloat:** Max 50 строк per file, FIFO для decisions
- **Middleware overhead:** Append-only writes, ~5 строк per update
- **27 commands to modify:** Partial rollout: core 5 commands first

## Требования (ссылки на REQ)

- `REQ-SESS-001` (P2): Session state structure и storage
- `REQ-SESS-002` (P2): Middleware pattern для автоматического обновления
- `REQ-SESS-003` (P2): `/speckit-continue` command
- `REQ-SESS-004` (P2): Selective context loading из session state
- `REQ-SESS-005` (P3): Multi-initiative session switching

## Приёмка

- Acceptance tests: Full lifecycle — start → prd → close → reopen → continue → verify state
- Definition of done: `.specify/memory/constitution.md#профили` (Minimal)
