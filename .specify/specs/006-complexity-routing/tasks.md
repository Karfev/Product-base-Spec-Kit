# Tasks: 006-complexity-routing

**Initiative:** INIT-2026-006-smart-discovery
**Owner:** @dmitriy

## Task list

- [ ] **T1:** Создать `.specify/memory/risk-keywords.yml` — словарь risk-keywords (high_risk, medium_risk) с pattern, min_profile, reason
- [ ] **T2a:** Определить acceptance tests — 3 сценария: Minimal auto-detect, Standard risk-keyword catch, Extended GDPR catch
- [ ] **T2b:** Создать `.claude/commands/speckit-quick.md` — command file с routing logic (keyword scan → component count → profile suggestion → init.sh call)
- [ ] **T3:** Модифицировать `.claude/commands/speckit-start.md` — добавить routing choice: quick vs full profile
- [ ] **T4:** Обновить `docs/QUICKSTART.md` — добавить секцию "Быстрый старт с /speckit-quick"
- [ ] **T5:** Обновить `CHANGELOG.md` инициативы

## Definition of done (Minimal profile)

| Checkpoint | Required |
|---|---|
| requirements.yml filled | MUST |
| spec/plan/tasks.md filled | MUST |
| Command file created | MUST |
| 3 acceptance scenarios passed | MUST |
| QUICKSTART.md updated | MUST |
| CI gates green | MUST |
