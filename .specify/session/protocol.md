# Session Update Protocol

> Shared middleware for all `/speckit-*` commands. Referenced from each command file.

## 8-Step Protocol

After successful command completion:

1. **Read/Create** session file `.specify/session/{INIT-ID}.md`
   - If not found → create from `.specify/session/TEMPLATE.md`, fill `{INIT-ID}`, `{profile}`, `{phase}`
2. **Update header:** set `**Last command:**` to current command + ISO timestamp
3. **Mark progress:** set current command to `[x]` in Progress checklist
4. **Compute next:** per lifecycle sequence below (utility commands: preserve existing `**Next:**`)
5. **Append decisions:** add key decisions from this session to Decisions section (FIFO, keep last 10)
6. **Sync open questions:** from relevant spec.md or prd.md
7. **Update context files:** set files list per phase→files table below
8. **Write back** to `.specify/session/{INIT-ID}.md`

## Lifecycle Sequence (for next-command computation)

```text
start → prd → requirements → contracts → specify → plan → tasks → implement → trace → rtm → consilium → graduate
```

## Command Adaptation Table

| Command | Type | Next | INIT-ID source |
|---|---|---|---|
| speckit-start | lifecycle | speckit-prd | Generated from Q1 |
| speckit-prd | lifecycle | speckit-requirements | $ARGUMENTS |
| speckit-requirements | lifecycle | speckit-contracts | $ARGUMENTS |
| speckit-contracts | lifecycle | speckit-specify | $ARGUMENTS |
| speckit-specify | lifecycle | speckit-plan | From spec.md Initiative field |
| speckit-plan | lifecycle | speckit-tasks | $ARGUMENTS (spec slug) |
| speckit-tasks | lifecycle | speckit-implement | $ARGUMENTS |
| speckit-implement | lifecycle | speckit-trace | $ARGUMENTS |
| speckit-trace | lifecycle | speckit-rtm | $ARGUMENTS |
| speckit-rtm | lifecycle | speckit-consilium | $ARGUMENTS |
| speckit-consilium | lifecycle | speckit-graduate | $ARGUMENTS |
| speckit-graduate | terminal | _(mark session complete)_ | $ARGUMENTS |
| speckit-release-rollout | lifecycle | contextual | $ARGUMENTS |
| _all other commands_ | utility | _(preserve current next)_ | $ARGUMENTS or context |

## Phase → Context Files Table (for selective loading)

| Phase | Always Load | Load Additionally | Skip |
|---|---|---|---|
| Any resume | `.specify/session/{INIT-ID}.md` | — | Full constitution |
| L3: PRD | — | `requirements.yml`, `domains/*/glossary.md` | Contracts, specs |
| L3: Requirements | — | `prd.md`, `requirements.yml` | Contracts, specs |
| L3: Contracts | — | `requirements.yml`, existing contracts | PRD, specs |
| L4: specify/plan | — | `spec.md`, `requirements.yml` | PRD, contracts |
| L4: tasks | — | `plan.md`, `spec.md` | PRD, contracts |
| L4: implement | — | `tasks.md`, `tools/ai-quality-gates.md` | PRD, other specs |
| L4: trace | — | `requirements.yml`, `contracts/*`, test files | PRD, specs |
| L5: evidence | — | `requirements.yml`, `trace.md` | PRD, specs |

## Selective Context Loading (command preamble)

When a command starts, BEFORE reading full context:
1. Check if `.specify/session/{INIT-ID}.md` exists
2. **If YES (resume):** read session file (~50 lines) + load only files from "Context Files" section
   - If any Context File is missing → fall back to full context load
3. **If NO (fresh start):** read full context as currently designed (no change)
