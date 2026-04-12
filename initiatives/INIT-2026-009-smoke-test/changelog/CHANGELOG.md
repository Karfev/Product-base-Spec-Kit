# Changelog

All notable changes to this initiative will be documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
Versioning: [SemVer](https://semver.org/)

## [Unreleased]

### Added

- REST API for exporting project reports (POST /exports, GET /exports/{id})
- JSON and CSV export format support
- Async export processing with queue-based architecture
- Event notification (export.completed) on export completion
- SLO: export latency P95 < 30s
- Feature flag: platform.exports.enabled

## [0.1.0] - 2026-04-12

### Added

- Initial specification draft.
