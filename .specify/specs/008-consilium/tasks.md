# Tasks: 008-consilium

**Initiative:** INIT-2026-007-quality-augmentation
**Owner:** @dmitriy

## Task list

- [x] **T1:** Создать `.specify/memory/consilium-roles.yml` — 5 базовых ролей (arch, security, db-load, infra, integrations) + 3 preset'а (standard, archkom-l1, archkom-l2)
- [x] **T2a:** Определить acceptance tests — PoC: прогнать consilium на PLAT-0003-async-queue, проверить формат output vs ADR-template-v2
- [x] **T2b:** Создать `.claude/commands/speckit-consilium.md` — command с sequential role execution, context loading, aggregation, ADR section injection
- [x] **T3:** PoC validation — запустить на PLAT-0003, оценить качество review (реальные findings vs формальные "OK")
- [x] **T4:** Документация — добавить секцию "Consilium" в README.md, обновить AGENTS.md с новым command
- [x] **T5:** Обновить `CHANGELOG.md` инициативы

## Definition of done (Minimal profile)

| Checkpoint | Required |
|---|---|
| requirements.yml filled | MUST |
| spec/plan/tasks.md filled | MUST |
| consilium-roles.yml created | MUST |
| Command file created | MUST |
| PoC on real ADR passed | MUST |
| Output format = ADR-template-v2 compatible | MUST |
| CI gates green | MUST |
