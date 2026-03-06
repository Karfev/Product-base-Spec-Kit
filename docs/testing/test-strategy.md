# Test Strategy Matrix

Этот документ задаёт обязательное сопоставление между типом требования, типом теста и стандартной командой запуска.

## Matrix

| Requirement type | Test type | Когда обязателен | Обязательная команда |
|---|---|---|---|
| functional | unit | Всегда для изменений бизнес-логики и pure functions | `make test-unit` |
| functional | contract | Для профилей **Standard/Extended** и любых изменений API/событийных контрактов | `make test-contract` |
| functional | integration | Когда есть взаимодействие с БД, внешним сервисом, очередью, файловым хранилищем | `make test-integration` |
| nfr | perf | Для NFR по latency/throughput/capacity/scalability | `make test-perf` |

## Usage in task planning

- **T2a (RED):** запускать обязательные команды из матрицы для выбранных требований и фиксировать, что тесты падают.
- **T2b (GREEN):** после реализации запускать те же команды и фиксировать успешный результат.
- **T3:** обязательно запускать `make test-integration`, если интеграционный сценарий применим.
- Для NFR-проверок производительности добавлять отдельную задачу с `make test-perf`.

## Entrypoint conventions

Стандартизированные точки входа определены в `Makefile`:

- `make test-unit`
- `make test-contract`
- `make test-integration`
- `make test-perf`

При необходимости команда может быть переопределена через переменные окружения:

- `TEST_UNIT_CMD`
- `TEST_CONTRACT_CMD`
- `TEST_INTEGRATION_CMD`
- `TEST_PERF_CMD`
