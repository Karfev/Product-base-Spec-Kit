# INIT-2026-007-quality-augmentation

| Поле | Значение |
|---|---|
| **Initiative** | INIT-2026-007-quality-augmentation |
| **Profile** | Minimal |
| **Status** | Active |
| **Owner** | @dmitriy |
| **Last updated** | 2026-04-12 |

## Описание

Два P1 улучшения SpecKit по результатам анализа конкурента Datarim:
1. **Consilium** — `/speckit-consilium` для structured multi-perspective review ADR, с ролями из доменной модели Архкомма (ИБ, БД/нагрузки, инфраструктура, интеграции, прикладная архитектура)
2. **AI Quality Gates** — `tools/ai-quality-gates.md` + enforcement в `/speckit-implement` (decomposition, architecture-first, test-first, contract-aware)

## Artifact Status

| Артефакт | Статус |
|---|---|
| prd.md | Draft |
| requirements.yml | Draft (6 REQs) |
| CHANGELOG.md | Initial |

## L4 Specs

| Spec | Slug | REQs | Статус |
|---|---|---|---|
| 008 | consilium | REQ-QUAL-001, REQ-QUAL-002, REQ-QUAL-003, REQ-QUAL-006 | Draft |
| 010 | ai-quality-gates | REQ-QUAL-004, REQ-QUAL-005 | Draft |

## Related

- **Source analysis:** `CLAUDE OUTPUTS/SpecKit/SpecKit_Datarim-Analysis_Report_v1.md`
- **Competitor:** [Arcanada-one/datarim](https://github.com/Arcanada-one/datarim) — consilium.md, ai-quality.md skills
- **Domain model:** Архкомм ADR-template-v2 (доменные оценки), ADR-template-L1-minimal
- **Depends on:** INIT-2026-006-smart-discovery (P0 items, run first)
- **ADR for PoC:** `products/platform/decisions/PLAT-0003-async-queue.md`
