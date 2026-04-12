# INIT-2026-008-session-state

| Поле | Значение |
|---|---|
| **Initiative** | INIT-2026-008-session-state |
| **Profile** | Minimal |
| **Status** | Active |
| **Owner** | @dmitriy |
| **Last updated** | 2026-04-12 |

## Описание

Session state management: `.specify/session/` directory, middleware auto-update, `/speckit-continue` для seamless resume, selective context loading. Вдохновлено Datarim `datarim/` directory pattern.

## Artifact Status

| Артефакт | Статус |
|---|---|
| prd.md | Draft |
| requirements.yml | Draft (5 REQs) |
| CHANGELOG.md | Initial |

## L4 Specs

| Spec | Slug | REQs | Статус |
|---|---|---|---|
| 011 | session-context | REQ-SESS-001, REQ-SESS-002, REQ-SESS-004 | Draft |
| 012 | speckit-continue | REQ-SESS-003, REQ-SESS-005 | Draft |

## Related

- **Source:** Datarim `datarim/activeContext.md`, `/dr-continue`
- **Depends on:** INIT-2026-006 (P0, implemented), INIT-2026-007 (P1, implemented)
