# NFR Baseline: {product}

**Профиль:** Standard+
**Последнее обновление:** {YYYY-MM-DD}

## Privacy

| Требование | Уровень | Описание |
|---|---|---|
| Data classification | MUST | {классификация данных продукта} |
| Data retention | MUST | {сроки хранения} |
| PII handling | MUST | {как обрабатывается PII} |

## Security

| Требование | Уровень | Описание |
|---|---|---|
| Authentication | MUST | {механизм аутентификации} |
| Authorization | MUST | {модель авторизации} |
| Secrets management | MUST | {как управляются секреты} |

## Reliability

| Метрика | Target | Метод измерения |
|---|---|---|
| Availability | {99.9%} | SLO в `ops/slo.yaml` |
| Latency P95 | {300ms} | APM |
| Error rate | {<0.1%} | APM |
