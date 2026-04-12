# INIT-2026-006-smart-discovery

| Поле | Значение |
|---|---|
| **Initiative** | INIT-2026-006-smart-discovery |
| **Profile** | Minimal |
| **Status** | Active |
| **Owner** | @dmitriy |
| **Last updated** | 2026-04-12 |

## Описание

Два P0 улучшения SpecKit по результатам анализа конкурента Datarim:
1. **Complexity-Aware Auto-Routing** — `/speckit-quick` для автоматического определения профиля
2. **Codebase-First Discovery** — proposed answers в `/speckit-prd` на основе существующих L1/L2/L3 артефактов

## Artifact Status

| Артефакт | Статус |
|---|---|
| prd.md | Draft |
| requirements.yml | Draft (6 REQs) |
| CHANGELOG.md | Initial |

## L4 Specs

| Spec | Slug | REQs | Статус |
|---|---|---|---|
| 006 | complexity-routing | REQ-DISC-001, REQ-DISC-002, REQ-DISC-006 | Draft |
| 007 | codebase-first-discovery | REQ-DISC-003, REQ-DISC-004, REQ-DISC-005 | Draft |

## Related

- **Source analysis:** `CLAUDE OUTPUTS/SpecKit/SpecKit_Datarim-Analysis_Report_v1.md`
- **Competitor:** [Arcanada-one/datarim](https://github.com/Arcanada-one/datarim)
- **Depends on:** INIT-2026-004-adoption-path (REQ-ADOPT-007 SLO: time-to-first-validate ≤ 30 min)
