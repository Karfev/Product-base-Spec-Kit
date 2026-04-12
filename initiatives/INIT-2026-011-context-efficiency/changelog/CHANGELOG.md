# Changelog — INIT-2026-011-context-efficiency

All notable changes to this initiative are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/), [SemVer](https://semver.org/).

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
