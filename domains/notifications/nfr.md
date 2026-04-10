# NFR: notifications domain
Owner: @platform-team | Updated: 2026-04-10

Non-functional constraints for all services in this domain.

## Data Classification
PII — notification preferences содержат user_id и косвенно раскрывают интересы пользователя (какие категории включены/выключены). Классификация: **Personal / Internal**.

## Compliance
- **GDPR:** Пользователь имеет право отписаться от любых не-mandatory уведомлений. Opt-out должен быть реализован и аудируем.
- **SOC2:** Логирование изменений предпочтений для audit trail.
- **PCI-DSS:** Не применимо (нет финансовых данных).

## Cross-cutting Security
- Аутентификация: Bearer token (JWT) обязателен для всех API endpoints.
- Авторизация: Пользователь может изменять только свои предпочтения.
- Encryption: TLS 1.2+ для транспорта, at-rest encryption для хранилища предпочтений.
