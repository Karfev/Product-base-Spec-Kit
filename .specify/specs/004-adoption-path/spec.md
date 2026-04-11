# Spec: 004-adoption-path

**Initiative:** INIT-2026-004-adoption-path
**Profile:** Standard
**Owner:** @karfev
**Last updated:** 2026-04-11

## Summary

Add progressive onboarding to SpecKit: unified `/speckit-start` command, `upgrade.sh` for profile migration, QUICKSTART.md for new users, `/speckit-trace-viz` for traceability visualization, and decouple Archkom from Enterprise profile.

## Motivation / Problem

SpecKit requires 2-4 weeks of learning before first validated artifact. New users face cognitive overload with 5 layers, 4 profiles, and 24 commands. This blocks adoption beyond the framework author. See PRD: `../../../initiatives/INIT-2026-004-adoption-path/prd.md`.

## Scope

- REQ-ADOPT-001: `/speckit-start` unified entry command (5 questions to validated initiative)
- REQ-ADOPT-002: Clean Minimal scaffold (4 files only, no empty dirs)
- REQ-ADOPT-003: `upgrade.sh` profile migration (Minimal to Standard to Extended)
- REQ-ADOPT-004: Gate 1 Quick Start document (<=60 lines)
- REQ-ADOPT-005: `/speckit-trace-viz` Mermaid visualization
- REQ-ADOPT-006: Archkom decoupling from Enterprise profile
- REQ-ADOPT-007: Time-to-first-validate SLO (<=30 minutes)

## Non-goals

- Web UI or SaaS version
- Jira/Confluence/Notion integration
- Video tutorials
- Auto-migration from existing PRD formats

## API/Contracts

No contract changes. This initiative adds CLI tooling (init.sh changes, new upgrade.sh) and Claude Code commands (speckit-start, speckit-trace-viz). No REST API or event-driven contracts are introduced.

## Test strategy

- Unit: Shell script tests for init.sh archkom decoupling and upgrade.sh profile migration
- Integration: End-to-end scaffold + upgrade + validate pipeline
- Acceptance: User testing of Gate 1 flow (target: <30 minutes)

## Rollout

- Flag/guardrail: No feature flags needed. Changes are additive (new commands, new script). Archkom decoupling is backward-compatible.
- Migration: Existing initiatives unaffected. upgrade.sh creates backups before changes.
- Monitoring: GitHub issues and user feedback for adoption metrics.

## User stories

- As a new adopter, I want to run one command and get a validated initiative, so that I can try SpecKit without reading the full documentation.
- As a growing team, I want to upgrade my Minimal initiative to Standard, so that I can add contracts and traceability without starting over.
- As any user, I want to see a visual trace diagram, so that I understand why traceability matters.

## Requirements

- `REQ-ADOPT-001` (P0): Unified entry command `/speckit-start`
- `REQ-ADOPT-002` (P0): Clean Minimal scaffold
- `REQ-ADOPT-003` (P1): Profile upgrade path via `upgrade.sh`
- `REQ-ADOPT-004` (P0): Gate 1 Quick Start document
- `REQ-ADOPT-005` (P1): Traceability visualization via `/speckit-trace-viz`
- `REQ-ADOPT-006` (P1): Archkom decoupling from Enterprise
- `REQ-ADOPT-007` (P0): Time-to-first-validate SLO

## Acceptance criteria

- Given a new user runs /speckit-start, when they answer 5 questions, then make validate passes
- Given a Minimal initiative, when upgrade.sh --profile standard runs, then all Standard artifacts are added
- Given QUICKSTART.md, when a new user follows it, then they complete Gate 1 in under 30 minutes
- Given init.sh --profile standard without --preset archkom, when scaffold completes, then brd.md and hld.md do not exist

## Open Questions

| # | Question | Owner | Deadline | Status |
|---|----------|-------|----------|--------|
| 1 | Should /speckit-start support profiles beyond Minimal? | @karfev | 2026-04-15 | resolved |
| 2 | Where to store .backup/ directory? | @karfev | 2026-04-15 | resolved |
| 3 | Should QUICKSTART.md reference /speckit-start? | @karfev | 2026-04-15 | resolved |
