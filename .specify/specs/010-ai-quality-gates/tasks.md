# Tasks: 010-ai-quality-gates

**Initiative:** INIT-2026-007-quality-augmentation
**Owner:** @dmitriy

## Task list

- [x] **T1:** Создать `tools/ai-quality-gates.md` — Five Pillars (Decomposition, Test-First, Architecture-First, Focused Work, Contract-Aware) с правилами, примерами, anti-patterns
- [x] **T2a:** Определить acceptance tests — 3 сценария: T2a enforcement, decomposition prompt, contract mismatch detection
- [x] **T2b:** Модифицировать `.claude/commands/speckit-implement.md` — добавить pre-flight checklist перед T2b (read quality gates → check pre-conditions → warn/proceed)
- [x] **T3:** Расширить `tools/scripts/check-spec-quality.py` — добавить `check_task_ordering()`: T2b without T2a → CI warning
- [x] **T4:** Тестирование — прогнать на INIT-2026-009-smoke-test tasks.md (T2b checked, T2a should be checked too)
- [x] **T5:** Обновить `CHANGELOG.md` инициативы

## Definition of done (Minimal profile)

| Checkpoint | Required |
|---|---|
| requirements.yml filled | MUST |
| spec/plan/tasks.md filled | MUST |
| ai-quality-gates.md created | MUST |
| speckit-implement.md modified | MUST |
| check-spec-quality.py extended | MUST |
| 3 acceptance scenarios passed | MUST |
| CI gates green | MUST |
