# Changelog

All notable changes to INIT-2026-007-quality-augmentation.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [SemVer](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-04-12

### Added

- `/speckit-consilium` — multi-perspective ADR review command (REQ-QUAL-001, REQ-QUAL-003)
- `.specify/memory/consilium-roles.yml` — 5 domain roles + 3 Архкомм presets (REQ-QUAL-002, REQ-QUAL-006)
- `tools/ai-quality-gates.md` — Five Pillars of AI Quality (REQ-QUAL-004)
- PoC consilium review on PLAT-0003-async-queue (standard preset, 3 roles)

### Changed

- `/speckit-implement` — added pre-flight checklist before T2b (REQ-QUAL-005)
- `check-spec-quality.py` — added T2b-before-T2a ordering detection (REQ-QUAL-005)
- All 6 REQ-IDs status: draft → implemented

## [0.1.0] - 2026-04-12

### Added

- Initial PRD with 2 P1 features: consilium (multi-perspective ADR review), AI quality gates
- requirements.yml with 6 REQs (4 P1, 1 P2)
- L4 specs: 008-consilium, 010-ai-quality-gates
