---
graduated_from: docs/plans/2026-04-12-quality-augmentation-design.md, docs/testing/test-strategy.md
date: 2026-04-13
type: design-pattern
---

# Quality Governance Patterns

## Consilium: Multi-Perspective ADR Review

Sequential role-switching pattern for architecture decision review. One agent evaluates an ADR from multiple domain perspectives, producing structured verdicts.

### Algorithm

1. **Determine panel:** `--preset` flag → preset from `consilium-roles.yml`; auto → profile mapping (Standard→standard, Extended→archkom-l1, Enterprise→archkom-l2)
2. **For each role (sequential):** load role definition + context files → read ADR → evaluate checklist → verdict (OK / Замечание / Блокер)
3. **Aggregate:** Any Блокер → "требует доработки"; only Замечания → "одобрено с условиями"; all OK → "одобрено"
4. **Inject** "Доменные оценки" section into ADR

Base roles: arch, security, db-load, infra, integrations. Extensible via `.specify/memory/consilium-roles.yml`.

## Five Pillars: AI Quality Constraints

Quality constraints enforced in `/speckit-implement` and backed by CI.

| Pillar | Rule | Enforcement |
|---|---|---|
| Decomposition | Max 50 LOC per function | Agent prompt |
| Test-First | T2a (RED) before T2b (GREEN) | Agent prompt + `check-spec-quality.py` |
| Architecture-First | Stubs before logic; stubs match contracts | `make lint-contracts` |
| Focused Work | One task = one bounded context | Agent prompt |
| Contract-Aware | Implementation matches OpenAPI/AsyncAPI | `make lint-contracts` |

## Test Ordering Matrix

| Requirement type | Test type | When mandatory | Command |
|---|---|---|---|
| functional | unit | Always for business logic / pure functions | `make test-unit` |
| functional | contract | Standard+ profiles, any API/event contract changes | `make test-contract` |
| functional | integration | DB, external service, queue, or file storage interaction | `make test-integration` |
| nfr | perf | NFR by latency/throughput/capacity/scalability | `make test-perf` |

**Task ordering:** T2a runs mandatory commands and verifies RED (failing). T2b runs same commands and verifies GREEN (passing). T3 always runs `make test-integration` if applicable.

## Key Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Role definitions format | YAML config | Extensible without modifying command |
| Execution model | Sequential role switching | No coordination complexity |
| Quality gates format | Markdown | Agent reads and interprets naturally |
| Enforcement | Agent prompts + CI backup | Primary: prompt in implement, safety net: check-spec-quality.py |
| Scope | Standard+ only | Minimal = quick fix, overhead unjustified |

## References

- Consilium roles: `.specify/memory/consilium-roles.yml`
- Quality gates enforcement: `.claude/commands/speckit-implement.md`
- CI script: `tools/scripts/check-spec-quality.py`
