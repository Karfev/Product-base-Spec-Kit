# PRD: Multi-Agent Portability — OpenCode & Kilo Code

**Initiative:** INIT-2026-005-multi-agent-portability
**Owner (PM):** @karfev
**Last updated:** 2026-04-11
**Profile:** Standard

---

## Цель и ожидаемый эффект

- **Проблема:** SpecKit привязан к Claude Code через `.claude/commands/` и `CLAUDE.md`. Команды, работающие с on-premise LLM, не могут использовать SpecKit без Anthropic API. Это блокирует adoption для air-gapped окружений и организаций с требованиями data residency.
- **Почему сейчас:** OpenCode (131K stars на GitHub) и Kilo Code (1.5M пользователей) поддерживают стандарт SKILL.md (с декабря 2025). Оба агента работают с локальными LLM через Ollama/vLLM, что открывает путь к полной on-premise портативности.
- **Цель (Outcome):** Команды, использующие OpenCode или Kilo Code с on-premise LLM, проходят полный SpecKit workflow (init -> prd -> requirements -> spec -> plan -> tasks -> implement -> trace -> rollout -> evidence) без обращения к Anthropic API.

## Пользователи и сценарии

- **Primary personas:**
  - On-Prem Team — работают в air-gapped окружении или подчинены требованиям data residency; не могут использовать cloud API
  - OpenCode Adopter — разработчик, использующий OpenCode как основной AI coding agent с локальной или cloud LLM
  - Kilo Code IDE User — разработчик в VS Code или JetBrains, использующий Kilo Code extension с Ollama/vLLM backend

- **Top JTBD / сценарии:**
  1. On-Prem Team хочет запустить `./tools/init.sh` + все `/speckit-*` команды в OpenCode с Qwen2.5-Coder-32B через Ollama, чтобы вести requirements-driven development без cloud зависимости
  2. OpenCode Adopter хочет получить `AGENTS.md` с полным каталогом навыков и запустить `/speckit-start` в OpenCode, чтобы онбордиться за <60 минут
  3. Kilo Code IDE User хочет использовать `/speckit-implement` из VS Code с локальной LLM, чтобы получить guided implementation без переключения в терминал

## Метрики успеха

| Метрика | Baseline | Target | Период | Источник |
|---|---:|---:|---|---|
| % команд, совместимых с OpenCode и Kilo Code | 0% | >90% (22 из 26) | 30d | Smoke-test matrix |
| Time-to-first-validate on-prem (OpenCode + Ollama) | N/A | <60 min | 30d | Manual test |
| "Claude Code only" issues на GitHub | N/A | 0 | 90d | GitHub Issues |

## Scope

**In-scope:**

- `AGENTS.md` — единый каталог навыков с маршрутизацией по агентам (Claude Code, OpenCode, Kilo Code) -> `REQ-PORT-001`
- Верификация всех 26 команд в OpenCode -> `REQ-PORT-002`
- Верификация всех 26 команд в Kilo Code (VS Code + JetBrains) -> `REQ-PORT-003`
- Setup guide для OpenCode (`docs/SETUP-OPENCODE.md`) -> `REQ-PORT-004`
- Setup guide для Kilo Code (`docs/SETUP-KILOCODE.md`) -> `REQ-PORT-005`
- Compatibility matrix (`docs/COMPAT-MATRIX.md`) — какие команды работают в каком агенте -> `REQ-PORT-006`
- ADR по выбору модели для on-premise deployment -> `REQ-PORT-007`
- Agent-neutral language в README и документации -> `REQ-PORT-008`

**Non-goals:**

- Поддержка Aider, Continue, Goose, Cursor, Windsurf (отдельные инициативы по мере запроса)
- Поддержка Codex CLI (нет SKILL.md/custom commands)
- Web UI для SpecKit
- Fine-tuning или адаптация моделей под SpecKit промпты

## Риски и ограничения

- **Качество output от локальных LLM:** Open-weight модели (Qwen2.5-Coder-32B) могут генерировать YAML с ошибками чаще, чем Claude Opus. Mitigation: smoke-test matrix + документирование known limitations, fallback на Qwen2.5-Coder-14B для простых команд.
- **Контекстное окно:** Практическое окно Qwen2.5-Coder-32B — 32K-64K токенов, не 128K. Mitigation: документировать в setup guides, рекомендовать split для больших кодовых баз.
- **Разница в поведении агентов:** OpenCode и Kilo Code интерпретируют SKILL.md по-разному. Mitigation: верификация каждой команды в каждом агенте, фиксация различий в COMPAT-MATRIX.

## Требования (ссылки на REQ)

Реестр требований — в `requirements.yml`. Здесь только ссылки:

- `REQ-PORT-001` (P0): AGENTS.md с полным каталогом навыков
- `REQ-PORT-002` (P0): Верификация 26 команд в OpenCode
- `REQ-PORT-003` (P0): Верификация 26 команд в Kilo Code
- `REQ-PORT-004` (P1): Setup guide для OpenCode
- `REQ-PORT-005` (P1): Setup guide для Kilo Code
- `REQ-PORT-006` (P1): Compatibility matrix
- `REQ-PORT-007` (P1): ADR по выбору модели
- `REQ-PORT-008` (P1): Agent-neutral language в README

## Приёмка

- Acceptance tests: Smoke-test 5 ключевых команд (`/speckit-start`, `/speckit-prd`, `/speckit-requirements`, `/speckit-implement`, `/speckit-trace`) в OpenCode и Kilo Code с on-premise LLM
- `make validate` проходит на артефактах, созданных on-premise агентом
- Definition of done по профилю: `.specify/memory/constitution.md#профили`
