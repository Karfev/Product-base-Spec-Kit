# Changelog — INIT-2026-011-context-efficiency

All notable changes to this initiative are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/), [SemVer](https://semver.org/).

## [0.4.0] — 2026-04-12

### Added
- Enhanced `protocol.md` with full Phase→Context Files loading matrix (presets + indexes) (REQ-CTX-006)
- Context loading preamble with `--full-context` escape hatch in all 13 lifecycle commands (REQ-CTX-006)
- Context Loading Rules section in `constitution.md` (REQ-CTX-005)

### Changed
- Updated 4 existing preambles (prd, requirements, contracts, specify) to reference protocol.md phase table

## [0.3.0] — 2026-04-12

### Added
- Index generation hook in `/speckit-requirements` — auto-generates `requirements-index.md` (REQ-CTX-003)
- Index generation hook in `/speckit-contracts` — auto-generates `contracts-index.md` (REQ-CTX-004)
- `tools/scripts/check-index-stale.py` — SHA-256 stale detection for indexes (REQ-CTX-007)
- `check-index-stale` Makefile target, added to `check-all` chain

### Changed
- 7 commands updated to read `requirements-index.md` instead of full `requirements.yml` (REQ-CTX-005)
  - L4: implement, plan, tasks, specify
  - L3 read: prd (cross-scan)
  - Governance: graduate, consilium

## [0.2.0] — 2026-04-12

### Added
- `.specify/memory/presets/archkom.md` — Архкомм governance preset (51 lines)
- `.specify/memory/presets/gsd.md` — GSD execution engine preset (57 lines)
- `.specify/memory/presets/README.md` — preset convention + reference links
- `.specify/memory/constitution-v1-full.md` — archived original constitution

### Changed
- Lean constitution refactoring: 298 → 139 lines (REQ-CTX-001)
- Preset loading in 7 commands: consilium, architecture, graduate, gsd-bridge, gsd-verify, gsd-map, implement (REQ-CTX-002)
- Permission boundaries refs in 3 GSD commands → presets/gsd.md

## [0.1.0] — 2026-04-12

### Added
- Initial PRD: Context Efficiency (lean constitution + context indexing + phase-gated loading)
- requirements.yml: 7 REQs (REQ-CTX-001..007), all status=draft
- L4 specs: 015-constitution-lean, 016-context-indexing, 017-phase-gated-loading
- README.md with key design decisions from brainstorm
