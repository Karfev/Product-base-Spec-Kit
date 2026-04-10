# Architecture: platform
Owner: @platform-team | Version: 0.1.0 | Updated: 2026-04-10

## 1. Introduction & Goals
Core platform services для управления пользователями, аутентификации и уведомлений. Ключевые цели качества: надёжность, безопасность, низкая латентность API.

## 2. Constraints
- TypeScript / Node.js runtime
- PostgreSQL как primary store
- Redis для кэширования и сессий
- RabbitMQ для асинхронных событий
- GDPR compliance обязателен

## 3. Context & Scope
{placeholder: system context diagram — what is inside/outside the system boundary}

## 4. Solution Strategy
{placeholder: key architectural decisions and technology choices}

## 5. Building Blocks
{placeholder: top-level components and their responsibilities}

## 6. Runtime Behaviour
{placeholder: key runtime scenarios / sequence diagrams}

## 7. Deployment
{placeholder: infrastructure, environments, deployment topology}

## 8. Crosscutting Concepts
{placeholder: security, observability, error handling patterns}

## 9. Architecture Decisions
→ See `../decisions/` for ADRs (format: `platform-NNNN-slug`)

## 10. Quality Requirements
→ See `../nfr-baseline/baseline.md` for measurable NFR targets
