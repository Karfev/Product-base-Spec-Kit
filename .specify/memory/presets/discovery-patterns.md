---
graduated_from: docs/plans/2026-04-12-smart-discovery-design.md
date: 2026-04-13
type: design-pattern
---

# Discovery Patterns: Auto-Routing + Codebase-First Elicitation

## Auto-Routing Algorithm

Reduces profiling from 8 questions to 1 description sentence for most cases.

### Steps

1. **Risk-keyword scan:** match user description against `risk-keywords.yml` patterns
   - `matched_high` → profile = max(kw.min_profile)
   - `matched_medium` ≥ 3 → profile = standard
   - else → profile = minimal
2. **Component count estimation:** count mentions of files/components/services/endpoints/tables/modules/contracts
   - \>15 → extended; >5 → standard
3. **Output:** if minimal + no high risk → scaffold immediately; else → show suggestion with risk warnings + offer override / full `/speckit-profile`

Override UP (Minimal→Standard): scaffold enhanced artifacts. Override DOWN (Standard→Minimal): warning about detected risks, require explicit confirm.

## Codebase-First Context Loading

Before each PRD question, scan existing L1/L2/L3 artifacts for proposed answers.

| PRD Question | Files to check | Section to extract |
|---|---|---|
| Problem / Goal | Last 3 L3 `initiatives/*/prd.md` | "Цель и ожидаемый эффект" |
| Tech stack | L2 `products/{product}/architecture/overview.md` | Technology, Stack |
| NFR targets | L2 `products/{product}/nfr-baseline/baseline.md` | All |
| Terminology | L1 `domains/*/glossary.md` | All |
| API patterns | Last 3 L3 `initiatives/*/contracts/openapi.yaml` | paths |
| Users / Scenarios | Last 3 L3 `initiatives/*/prd.md` | "Пользователи и сценарии" |

**Constraints:** max 3 files per question, skip archived initiatives, no semantic search (file path conventions only), staleness warning if source >90 days old.

## Discovery Depth Modes

| Mode | Questions | Trigger | Topics |
|---|---|---|---|
| Quick | 3-5 | profile = minimal | Problem, Scope, REQs, Risks (opt), Metrics (opt) |
| Standard | 5-10 | profile = standard | + Users, Architecture, Contracts, NFR, Dependencies |
| Deep | 10-15 | profile = extended+ | + Security, Compliance, Migration, Rollout, Cross-initiative |

Override: `--depth quick|standard|deep` flag on `/speckit-prd`.

## Key Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Risk keyword source | YAML config | Extensible, single source of truth |
| Profile routing | Heuristic with escape hatch | Speed + safety: always offers /speckit-profile fallback |
| Context loading | File path conventions, not semantic search | Predictable, offline, no dependencies |
| Proposed answers | Show source + date + confirm/deny | Prevents false confidence from stale data |

## References

- Risk keywords dictionary: `.specify/memory/risk-keywords.yml`
- Auto-routing entry point: `/speckit-quick`, `/speckit-start`
- Context loading in: `/speckit-prd`
