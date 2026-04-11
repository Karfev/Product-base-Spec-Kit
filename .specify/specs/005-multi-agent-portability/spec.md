# Spec: 005-multi-agent-portability

**Initiative:** INIT-2026-005-multi-agent-portability
**Profile:** Standard
**Owner:** @karfev
**Last updated:** 2026-04-11

## Summary

Port SpecKit to work with OpenCode and Kilo Code agents for on-premise LLM deployment. Create AGENTS.md universal entry point, compatibility matrix, setup guides for OpenCode (Ollama) and Kilo Code (VS Code/JetBrains), ADR for local model selection, and make all documentation agent-neutral.

## Motivation / Problem

SpecKit is perceived as Claude Code-only despite 22 of 26 commands being fully portable. On-premise teams with H100/RTX 6000 PRO Blackwell cannot use the framework without Anthropic API. OpenCode and Kilo Code support the SKILL.md standard but SpecKit has no documentation for these agents. See PRD: `../../../initiatives/INIT-2026-005-multi-agent-portability/prd.md`.

## Scope

- REQ-PORT-001: AGENTS.md universal entry point with skill catalog
- REQ-PORT-002: OpenCode compatibility verification (26 commands)
- REQ-PORT-003: Kilo Code compatibility verification (26 commands)
- REQ-PORT-004: docs/SETUP-OPENCODE.md on-premise guide
- REQ-PORT-005: docs/SETUP-KILOCODE.md IDE guide
- REQ-PORT-006: Agent compatibility table in README.md
- REQ-PORT-007: ADR model selection for H100 and RTX 6000 PRO
- REQ-PORT-008: On-premise latency SLO

## Non-goals

- Support for Aider, Continue, Goose, Cursor, Windsurf
- Codex CLI portability (cloud-only)
- Web UI or SaaS wrapper
- Fine-tuning local models
- Modifying existing SKILL.md command files

## API/Contracts

No contract changes. This initiative adds documentation (AGENTS.md, CLAUDE.md, setup guides, COMPAT-MATRIX), a symlink for OpenCode compatibility, and a CI validation script.

## Test strategy

- Unit: check-agents-md.py validates AGENTS.md references match .claude/commands/ files
- Integration: Smoke test 5 key commands on OpenCode and Kilo Code (requires hardware)
- Acceptance: New user follows SETUP guide, completes /speckit-start in under 60 minutes

## Rollout

- Flag/guardrail: All changes are additive. No existing behavior modified.
- Migration: CLAUDE.md redirects to AGENTS.md. .opencode/skills symlink is transparent.
- Monitoring: GitHub issues tracking "Claude Code only" complaints.

## User stories

- As an on-premise team, I want to run SpecKit with a local LLM on H100, so that I comply with data residency requirements without Anthropic API.
- As an OpenCode user, I want to invoke /speckit-start from my terminal, so that I can use SpecKit without switching to Claude Code.
- As a Kilo Code user, I want to run speckit commands from VS Code Command Palette, so that I stay in my IDE workflow.

## Requirements

- `REQ-PORT-001` (P0): AGENTS.md universal entry point
- `REQ-PORT-002` (P0): OpenCode compatibility verification
- `REQ-PORT-003` (P0): Kilo Code compatibility verification
- `REQ-PORT-004` (P1): OpenCode on-premise setup guide
- `REQ-PORT-005` (P1): Kilo Code IDE setup guide
- `REQ-PORT-006` (P1): Agent compatibility matrix in README
- `REQ-PORT-007` (P1): ADR local model selection
- `REQ-PORT-008` (P1): On-premise latency SLO

## Acceptance criteria

- Given AGENTS.md exists, when check-agents-md.py runs, then all 26 skills match files in .claude/commands/
- Given .opencode/skills symlink exists, when OpenCode opens the repo, then it discovers speckit skills
- Given README.md, when grep for "Claude Code" runs, then 0 results (except CLAUDE.md redirect)
- Given SETUP-OPENCODE.md, when followed on Ubuntu with Ollama, then /speckit-start succeeds without API key

## Open Questions

| # | Question | Owner | Deadline | Status |
|---|----------|-------|----------|--------|
| 1 | Does OpenCode support .claude/commands/ natively? | @karfev | 2026-04-15 | resolved: NO (issue #6985), use .opencode/skills symlink |
| 2 | DeepSeek-V3 on single GPU? | @karfev | 2026-04-15 | resolved: NOT feasible (671B MoE, ~380GB VRAM) |
| 3 | Practical context window of Qwen2.5-Coder-32B? | @karfev | 2026-04-15 | resolved: 32K-64K practical (not 128K claimed) |
