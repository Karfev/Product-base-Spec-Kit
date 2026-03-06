# Rollout Plan: INIT-2026-001-ontology-demo

## Стратегия развёртывания

- Feature flag: `platform.ontology_demo.enabled`

## Мониторинг

- SLO: `ops/slo.yaml#ci-validation-latency`

## Rollback

Триггер для отката: рост времени CI-валидации выше 30 секунд на P95.
