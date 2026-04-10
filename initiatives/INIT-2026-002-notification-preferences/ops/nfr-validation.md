# NFR Validation: INIT-2026-002-notification-preferences

**Профиль:** Extended
**Последнее обновление:** 2026-04-10

## Проверяемые NFR

| REQ-ID | Категория | Target | Метод валидации | Результат |
|---|---|---|---|---|
| `REQ-{SCOPE}-{NNN}` | performance | p95 < {300ms} | Load test (`tests/perf/`) | {pass\|fail\|pending} |
| `REQ-{SCOPE}-{NNN}` | reliability | availability > {99.9%} | Chaos engineering | {pass\|fail\|pending} |
| `REQ-{SCOPE}-{NNN}` | security | OWASP Top 10 | Penetration test | {pass\|fail\|pending} |

## Результаты нагрузочного тестирования

```text
{Сюда вставить вывод из JMeter / k6 / Gatling}
```

Отчёт: `evidence/perf-report-2026-04-10.html`

## Результаты security-сканирования

```text
{Сюда вставить summary из DAST / SAST / dependency check}
```

Отчёт: `evidence/security-report-2026-04-10.html`
