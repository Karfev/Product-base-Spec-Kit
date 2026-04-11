# Tasks: 005-multi-agent-portability

**Initiative:** INIT-2026-005-multi-agent-portability
**Owner:** @karfev

> Test strategy matrix: `docs/testing/test-strategy.md`

## Task list

- [x] **T1:** No contract changes needed. OpenAPI/AsyncAPI stubs marked as empty for this tooling initiative. (`make lint-contracts` passes)
- [x] **T2a:** Write CI validation: check-agents-md.py verifies bidirectional sync between AGENTS.md and .claude/commands/ files. Test confirms: missing reference = error, missing file = error.
- [x] **T2b:** Implement all changes: AGENTS.md, CLAUDE.md, .opencode/skills symlink, COMPAT-MATRIX.md, SETUP-OPENCODE.md, SETUP-KILOCODE.md, ADR model selection, README Agent Compatibility section, init.sh/QUICKSTART.md agent-neutral language, validate.yml CI step.
- [ ] **T3:** Integration tests on actual hardware: smoke test 5 key commands on OpenCode (Ollama + Qwen2.5-Coder-32B) and Kilo Code (VS Code + local endpoint). Requires H100 or RTX 6000 PRO.
- [ ] **T4:** Latency benchmarks (REQ-PORT-008): measure /speckit-prd wall-clock time on H100 and RTX 6000 PRO.
- [ ] **T5:** Update trace.md + changelog/CHANGELOG.md, run: `make check-trace`
- [ ] **T6:** PRR checklist review: `ops/prr-checklist.md` (Standard profile items)

## Definition of done (by profile)

| Checkpoint | Minimal | Standard | Extended |
|---|---|---|---|
| requirements.yml filled | MUST | MUST | MUST |
| spec/plan/tasks.md filled | MUST | MUST | MUST |
| Contracts valid (lint/validate) | — | MUST | MUST |
| trace.md filled | — | MUST | MUST |
| slo.yaml and prr-checklist.md | — | MUST | MUST |
| threat-model.md | — | — | MUST |
| CI gates green | MUST | MUST | MUST |
