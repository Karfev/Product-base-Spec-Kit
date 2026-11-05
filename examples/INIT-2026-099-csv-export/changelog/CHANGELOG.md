# Changelog: INIT-2026-099-csv-export

> Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
> Versioning: SemVer (`metadata.version` в [`requirements.yml`](../requirements.yml)).

## [Unreleased]

### Added

- Initial set of requirements REQ-EXPORT-001..005.
- ADR-0001 — hybrid sync/async strategy.
- OpenAPI 3.1 contract: `POST /export`, `GET /export/jobs/{jobId}`.
- AsyncAPI 3.0 contract: `export.job.completed`, `export.job.failed`.
- SLO: latency P95 < 5s, availability ≥ 99.5%.
- PRR checklist (status: amber).
- Rollout plan: feature flag, 3 этапа.

### Changed

- (none)

### Removed

- (none)

---

## [0.1.0] — 2026-04-28

### Added

- Initiative scaffold (Standard profile).
