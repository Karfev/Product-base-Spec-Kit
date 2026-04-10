# Event Catalog: notifications domain
Owner: @platform-team | Updated: 2026-04-10

Domain events published by this bounded context.

## Events

### notifications.preference.updated
**Description:** Пользователь изменил свои предпочтения уведомлений (канал, частоту или opt-out).
**Trigger:** Пользователь сохранил изменения в настройках уведомлений через API.
**Payload (key fields):** user_id, changed_fields[], previous_values, new_values
**Consumers:** notification-delivery-service (обновляет маршрутизацию), analytics (отслеживает opt-out rate)
**Channel:** notifications.preferences.updated

### notifications.category.opted-out
**Description:** Пользователь отписался от категории уведомлений.
**Trigger:** Пользователь отключил конкретную категорию через API или ссылку в email.
**Payload (key fields):** user_id, category_id, opt_out_source (api | email_link)
**Consumers:** compliance-service (GDPR audit trail), analytics
**Channel:** notifications.preferences.category-opted-out
