# Production Readiness Review: INIT-2026-005-multi-agent-portability

**Профиль:** Standard+
**Последнее обновление:** 2026-04-11
**Правило:** пункты с **P0** MUST быть закрыты до релиза (blocking gate).
**Источник практики:** Google SRE Book, глава PRR.

---

## Service levels (SLO/SLI)

- [ ] **P0** SLO определён в `ops/slo.yaml` (OpenSLO) и согласован
- [ ] **P0** SLI измеримы (источники метрик определены)
- [ ] P1 Error budget policy определена (если применимо)

## Architecture & dependencies

- [ ] **P0** Критические зависимости перечислены, есть деградация / таймауты / ретраи
- [ ] P1 Capacity / scaling предположения проверены
- [ ] P1 Зависимости имеют SLO или degraded mode

## Observability

- [ ] **P0** Метрики «golden signals» определены (latency / traffic / errors / saturation)
- [ ] **P0** Логи и трейсы коррелируемы (trace_id / request_id)
- [ ] P1 Дашборд + алерты определены
- [ ] P1 Runbook написан (ссылка: {ссылка на wiki/confluence/…})

## Deployment & rollback

- [ ] **P0** Rollout / rollback описаны (`delivery/rollout.md`)
- [ ] **P0** Миграции обратимы или есть runbook отката (`delivery/migration.md`)
- [ ] P1 Feature flags задокументированы


## Ops & on-call

- [ ] **P0** Runbook присутствует для P0/P1 инцидентов
- [ ] P1 SRE / on-call ownership согласован

---

## Итог PRR

| Блок | Статус | Комментарий |
|---|---|---|
| SLO/SLI | {open\|passed\|blocked} | {…} |
| Architecture | {open\|passed\|blocked} | {…} |
| Observability | {open\|passed\|blocked} | {…} |
| Deployment | {open\|passed\|blocked} | {…} |
| Ops | {open\|passed\|blocked} | {…} |

**Общий статус:** {open | passed | blocked}
**Дата последнего ревью:** 2026-04-11
**Ревьюер:** @{sre-or-reviewer}
