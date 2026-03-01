---
status: "proposed"
date: "2026-03-01"
decision-makers: ["@platform-team"]
consulted: ["@security-team", "@sre-team"]
informed: ["@product-team", "@support-team"]
---

# INIT-2026-000-ADR-0001: Bcrypt hashing for API key secrets

## Context and problem statement

API-ключи — долгосрочные credentials, которые необходимо хранить в базе данных. Если база данных будет скомпрометирована, секреты ключей не должны быть восстановимы. При этом каждый входящий запрос должен проходить валидацию с минимальными задержками (P95 < 10ms, см. REQ-AUTH-004).

Необходимо выбрать стратегию хранения секретов API-ключей, балансирующую безопасность, производительность и операционную простоту.

## Decision drivers

- **Безопасность:** Секреты не должны быть восстановимы при компрометации БД (нет plaintext, нет обратимого шифрования)
- **Производительность:** Накладные расходы аутентификации P95 < 10ms при стандартной нагрузке (1000 req/s) — требует кэширования
- **Простота:** Решение должно опираться на существующую инфраструктуру (PostgreSQL + Redis), без новых сервисов

## Considered options

- **Option A:** Plaintext storage — хранение секрета в открытом виде в PostgreSQL
- **Option B:** AES-256 encryption — шифрование секрета симметричным ключом, хранение зашифрованного blob в PostgreSQL
- **Option C:** Bcrypt hash (work_factor=10) + Redis cache — хэширование bcrypt, хранение хэша; Redis-кэш для fast-path аутентификации

## Decision outcome

**Chosen option:** "C — Bcrypt hash + Redis cache", because bcrypt необратим при компрометации БД (в отличие от AES, где компрометация ключа шифрования раскрывает все секреты), достаточно быстр при cache hit (< 1ms Redis lookup), и широко используется для хранения credentials.

**Детали реализации:**
- Work factor bcrypt = 10 (~100ms хэширования, выполняется только при создании ключа)
- Plaintext секрет возвращается пользователю единственный раз при создании и нигде не сохраняется
- Redis-кэш: ключ `api_key:{hash}`, TTL 60s, явная инвалидация при DELETE ключа
- Auth middleware: Redis lookup → если miss, PostgreSQL lookup + re-cache

### Consequences

- **Good:** Секреты необратимы при компрометации PostgreSQL без компрометации Redis и исходного секрета
- **Good:** Fast-path аутентификации через Redis cache обеспечивает P95 < 10ms при cache hit
- **Bad:** Потерянный секрет невозможно восстановить — пользователь обязан создать новый ключ
- **Neutral:** 60-секундное окно при компрометации ключа до полного распространения отзыва (явная инвалидация кэша минимизирует это окно на практике)

### Confirmation

Решение считается подтверждённым когда:
1. Нагрузочный тест `tests/perf/auth-latency.jmx` показывает P95 < 10ms при 1000 req/s
2. Тест `tests/api/api-keys.spec.ts::REQ-AUTH-001` подтверждает, что повторный GET не возвращает секрет
3. Тест `tests/api/api-keys.spec.ts::REQ-AUTH-002` подтверждает, что после revoke ключ отклоняется в течение 60s

---

*Шаблон основан на [MADR](https://adr.github.io/madr/) (включая YAML front-matter и Confirmation).*
