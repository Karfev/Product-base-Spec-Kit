# Tasks: 007-codebase-first-discovery

**Initiative:** INIT-2026-006-smart-discovery
**Owner:** @dmitriy

## Task list

- [ ] **T1:** Создать Question → File mapping table в plan.md (done) и формализовать как конфигурацию в speckit-prd.md
- [ ] **T2a:** Определить acceptance tests — 4 сценария: context found (L2), context found (L3 history), no context, stale context warning
- [ ] **T2b:** Модифицировать `.claude/commands/speckit-prd.md` — добавить context loading block, depth mode selector, proposed answer formatting
- [ ] **T3:** Тестирование на реальных данных — запустить модифицированный `/speckit-prd` для domain notifications (L1 glossary exists) и проверить proposed answers
- [ ] **T4:** Обновить `docs/QUICKSTART.md` — добавить секцию "Codebase-first Discovery"
- [ ] **T5:** Обновить `CHANGELOG.md` инициативы

## Definition of done (Minimal profile)

| Checkpoint | Required |
|---|---|
| requirements.yml filled | MUST |
| spec/plan/tasks.md filled | MUST |
| speckit-prd.md modified | MUST |
| 4 acceptance scenarios passed | MUST |
| QUICKSTART.md updated | MUST |
| CI gates green | MUST |
