---
graduated_from: docs/plans/2026-04-12-session-state-and-self-evolution-design.md
date: 2026-04-13
type: design-pattern
---

# Session State Protocol Design

## Summary

Shared middleware for persisting initiative state across `/speckit-*` commands. Enables resume capability and selective context loading. Session files are ephemeral (gitignored), per-initiative, max 50 lines.

## 8-Step Middleware Protocol

After successful command completion:

1. **Read/Create** session file `.specify/session/{INIT-ID}.md` (from TEMPLATE.md if new)
2. **Update header:** set `Last command` to current command + ISO timestamp
3. **Mark progress:** set current command to `[x]` in Progress checklist
4. **Compute next:** per lifecycle sequence (utility commands preserve existing Next)
5. **Append decisions:** key decisions from this session (FIFO, keep last 10)
6. **Sync open questions:** from relevant spec.md or prd.md
7. **Update context files:** set files list per phase→files table
8. **Write back** to session file

## Lifecycle Sequence

```
start → prd → requirements → contracts → specify → plan → tasks → implement → trace → rtm → consilium → graduate
```

## Phase → Context Files Table

| Phase | Always Load | Additionally | Skip |
|---|---|---|---|
| Any resume | session file | — | Full constitution |
| L3: PRD | — | requirements.yml, domains/*/glossary.md | Contracts, specs |
| L3: Requirements | — | prd.md, requirements.yml | Contracts, specs |
| L3: Contracts | — | requirements.yml, existing contracts | PRD, specs |
| L4: specify/plan | — | spec.md, requirements.yml | PRD, contracts |
| L4: tasks | — | plan.md, spec.md | PRD, contracts |
| L4: implement | — | tasks.md, tools/ai-quality-gates.md | PRD, other specs |
| L4: trace | — | requirements.yml, contracts/*, test files | PRD, specs |
| L5: evidence | — | requirements.yml, trace.md | PRD, specs |

## Selective Context Loading (command preamble)

1. Check if session file exists
2. **If YES (resume):** read session file (~50 lines) + load only files from "Context Files" section. If any missing → fall back to full context.
3. **If NO (fresh start):** read full context as currently designed (no change)

## Key Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Storage | Ephemeral (gitignored) | Session state is per-user, not shared |
| Scope | Per-initiative, max 50 lines | Prevents context bloat |
| Protocol location | Shared `.specify/session/protocol.md` | Single reference instead of per-command copy-paste |
| Evolution | Append-only `evolution-log.md` | Human-in-the-loop: proposals require manual PR |

## References

- Session template: `.specify/session/TEMPLATE.md`
- Protocol definition: `.specify/session/protocol.md`
- Constitution session rules: `.specify/memory/constitution.md` (lines 48-51)
