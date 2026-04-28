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
start → prd → requirements → contracts → specify → plan → tasks → implement → trace ╬═> rtm → consilium → graduate ──[optional]──> release-rollout
                                         └────────── L4 spec slug (NNN-slug) ─────────┘   └─────────────── L3 INIT-ID ───────────────────────────┘
```

> `╬═>` marks a **scope shift**: `trace` operates on an L4 spec (`<NNN>-<slug>`); `rtm` operates on an L3 initiative (`INIT-YYYY-NNN-slug`). The handoff requires reading `Initiative:` from `.specify/specs/<NNN>-<slug>/spec.md` and passing the resolved INIT-ID to `/speckit-rtm`.

> **release-rollout positioning:** runs after `graduate` for Standard+ profiles that ship to production. For Minimal profile it does not apply (see profile gate in the command). After release-rollout, the session ends; no automatic Next.

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
| speckit-trace | lifecycle | speckit-rtm | **From spec.md `Initiative:` field** — `$ARGUMENTS` is L4 spec slug (e.g. `001-user-auth`); rtm needs L3 INIT-ID. Resolve before handoff. |
| speckit-rtm | lifecycle | speckit-consilium | $ARGUMENTS (INIT-ID) |
| speckit-consilium | lifecycle | speckit-graduate | $ARGUMENTS |
| speckit-graduate | terminal | _(mark session complete)_ | $ARGUMENTS |
| speckit-release-rollout | lifecycle (Standard+ only; Minimal fails fast in profile gate) | _(terminal — session ends; no automatic Next)_ | $ARGUMENTS (INIT-ID) |
| _all other commands_ | utility | _(preserve current next)_ | $ARGUMENTS or context |

## Phase → Context Files Table (enhanced with presets + indexes)

| Phase | Constitution | Presets | Requirements | Contracts | Other |
|---|---|---|---|---|---|
| L3: PRD | lean | — | index (cross-scan) | — | `domains/*/glossary.md` |
| L3: Requirements | lean | — | **full** (write) | — | `prd.md` |
| L3: Contracts | lean | — | full | **full** (write) | — |
| L4: specify | lean | — | index + targeted REQs | — | `spec.md` |
| L4: plan | lean | — | index + targeted REQs | — | `spec.md` |
| L4: tasks | lean | — | index | — | `plan.md`, `spec.md` |
| L4: implement | lean | gsd (if GSD mode) | index | — | `tasks.md` |
| L5: trace/rtm | lean | — | **full** (needs traces) | full | test files |
| L5: evidence | lean | — | **full** | `trace.md` | — |
| Governance: consilium | lean | archkom | index | — | ADR files |
| Governance: graduate | lean | archkom (Standard+) | index | — | product registry |
| Architecture | lean | archkom | — | — | IS ontology |
| GSD: bridge/verify/map | lean | gsd | index | — | `.planning/*` |
| Any resume | session file | per phase | per phase | per phase | — |

**Legend:** lean = `.specify/memory/constitution.md`; index = `requirements-index.md`; full = `requirements.yml`

### Loading Rules

- **L3 write commands** (requirements, contracts): read full source files — they generate indexes
- **L4 commands** (specify, plan, tasks, implement): read index + targeted REQs from spec
- **Evidence commands** (trace, rtm, evidence): read full files — need trace fields
- **Governance** (consilium, graduate): read index for overview
- **Presets**: loaded only by commands that need them (see `.specify/memory/presets/README.md`)

### Escape Hatch

If `--full-context` is passed to any command, skip selective loading and read all files. Use when:
- Debugging unexpected behavior
- Cross-referencing across phases
- First run after major refactoring

## Selective Context Loading (command preamble)

When a command starts, BEFORE reading full context:
1. Check if `.specify/session/{INIT-ID}.md` exists
2. **If YES (resume):** read session file (~50 lines) + load only files from "Context Files" section per phase table above
   - If any Context File is missing → fall back to full context load
   - If `--full-context` flag → load all files (override)
3. **If NO (fresh start):** read full context as currently designed (no change)
