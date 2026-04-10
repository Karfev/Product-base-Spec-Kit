# Canonical Model: notifications domain
Owner: @platform-team | Updated: 2026-04-10

Core business objects and their relationships.

## Entities

### UserPreference
**Identity:** user_id (уникальный идентификатор пользователя в системе)
**Key attributes:** default_channel, digest_frequency, quiet_hours_start, quiet_hours_end
**Invariants:** У каждого пользователя ровно один набор предпочтений. digest_frequency ∈ {immediate, daily, weekly}.
**Relationships:** Содержит набор CategoryPreference (1:N). Привязан к User (из домена auth).
**Lifecycle:** created → active → (deactivated при удалении аккаунта)

### CategoryPreference
**Identity:** (user_id, category_id) — составной ключ
**Key attributes:** enabled (bool), channel_override (опциональный канал, отличный от default)
**Invariants:** Категории из списка security не могут быть отключены (enabled=false). channel_override если задан, должен быть из списка доступных каналов.
**Relationships:** Принадлежит UserPreference (N:1). Ссылается на NotificationCategory.
**Lifecycle:** opt-in (enabled=true) ↔ opt-out (enabled=false)

### NotificationCategory
**Identity:** category_id (slug, e.g. "security", "marketing", "billing")
**Key attributes:** name, description, is_mandatory (нельзя отключить)
**Invariants:** is_mandatory=true категории не могут быть отключены пользователем.
**Relationships:** Используется в CategoryPreference.
**Lifecycle:** Статический справочник, изменяется только администратором.

## Value Objects

### DigestFrequency
Перечисление: `immediate | daily | weekly`

### ChannelType
Перечисление: `email | push | sms`

## Aggregates

### UserPreference (Aggregate Root)
Граница консистентности: все CategoryPreference пользователя изменяются через UserPreference. Нельзя изменить CategoryPreference напрямую — только через операции агрегата.
