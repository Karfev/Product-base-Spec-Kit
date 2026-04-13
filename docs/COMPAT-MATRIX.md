# Agent Compatibility Matrix

Status of SpecKit skills across AI coding agents.

**Legend:** ✅ Full | ⚠️ Partial (workaround available) | ❌ Incompatible | ⏳ Untested

## Command Compatibility

| Skill | Claude Code | OpenCode | Kilo Code | Risk |
|-------|:-----------:|:--------:|:---------:|------|
| /speckit-start | ✅ | ⏳ | ⏳ | HIGH |
| /speckit-profile | ✅ | ⏳ | ⏳ | HIGH |
| /speckit-init | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-prd | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-requirements | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-contracts | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-specify | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-plan | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-tasks | ✅ | ⏳ | ⏳ | LOW |
| /speckit-implement | ✅ | ⏳ | ⏳ | HIGH |
| /speckit-trace | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-trace-viz | ✅ | ⏳ | ⏳ | LOW |
| /speckit-release-rollout | ✅ | ⏳ | ⏳ | HIGH |
| /speckit-prr-status | ✅ | ⏳ | ⏳ | LOW |
| /speckit-evidence | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-rtm | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-domain-init | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-domain-update | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-product-init | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-nfr-baseline | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-adr-product | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-architecture | ✅ | ⏳ | ⏳ | HIGH |
| /speckit-constitution-review | ✅ | ⏳ | ⏳ | HIGH |
| /speckit-gsd-bridge | ✅ | ⏳ | ⏳ | HIGH |
| /speckit-gsd-map | ✅ | ⏳ | ⏳ | HIGH |
| /speckit-gsd-verify | ✅ | ⏳ | ⏳ | HIGH |
| /speckit-consilium | ✅ | ⏳ | ⏳ | HIGH |
| /speckit-continue | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-graduate | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-quick | ✅ | ⏳ | ⏳ | MEDIUM |
| /speckit-reflect | ✅ | ⏳ | ⏳ | LOW |

## Capability Matrix

| Capability | Claude Code | OpenCode | Kilo Code |
|------------|:-----------:|:--------:|:---------:|
| $ARGUMENTS substitution | ✅ | ✅ | ✅ |
| File read/write | ✅ | ✅ | ✅ |
| Bash execution | ✅ | ✅ | ✅ |
| Multi-turn dialogue | ✅ | ✅ | ✅ |
| `.claude/commands/` discovery | ✅ | ❌ (use .opencode/skills symlink) | ✅ |
| AGENTS.md support | ✅ | ✅ | ✅ |

## Portability Risk Levels

- **LOW** (4 commands): Read-only reporting, no dialogue, simple file I/O
- **MEDIUM** (16 commands): Multi-turn dialogue, YAML generation, make validate calls
- **HIGH** (11 commands): Complex reasoning, decision trees, GSD integration, 16-question flows

## How to Run a Smoke Test

Test these 5 representative commands to verify agent compatibility:
1. `/speckit-profile INIT-2026-000-api-key-management` (multi-turn Q&A, decision tree)
2. `/speckit-prd INIT-2026-000-api-key-management` (5 questions, YAML refs, file write)
3. `/speckit-requirements INIT-2026-000-api-key-management` (REQ-ID generation, make validate)
4. `/speckit-specify 000-api-key-management` (multi-turn spec filling)
5. `/speckit-trace 000-api-key-management` (trace matrix generation)
