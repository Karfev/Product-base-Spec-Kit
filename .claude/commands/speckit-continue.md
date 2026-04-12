---
description: Resume from last checkpoint or show multi-initiative dashboard
argument-hint: [INIT-YYYY-NNN-slug] (optional)
---

You are helping the user resume work on a SpecKit initiative.

## Your job

1. **Discover sessions:** Glob `.specify/session/INIT-*.md` (skip TEMPLATE.md, protocol.md).

2. **Route by case:**

### Case A: No sessions found
Say: "Нет активных сессий. Запустить `/speckit-start` для новой инициативы?"
Stop.

### Case B: INIT-ID provided in $ARGUMENTS
1. Read `.specify/session/$ARGUMENTS.md`
2. If not found → "Сессия для $ARGUMENTS не найдена. Запустить `/speckit-start $ARGUMENTS`?"
3. If found → show **Summary** (see format below) + run **Stale Check**
4. Propose: "Продолжить с {next_command}? [Да / Другой command / Показать spec]"

### Case C: No argument, 1 session found
Auto-select the single session. Show **Summary** + **Stale Check**. Propose next command.

### Case D: No argument, 2+ sessions found
Show **Dashboard**:

```
┌──────────────────────────┬─────────┬──────────────┬──────────────┐
│ Initiative               │ Profile │ Phase        │ Next         │
├──────────────────────────┼─────────┼──────────────┼──────────────┤
│ {INIT-ID-1}              │ {prof}  │ {phase}      │ {next}       │
│ {INIT-ID-2}              │ {prof}  │ {phase}      │ {next}       │
└──────────────────────────┴─────────┴──────────────┴──────────────┘
```

Sorted by `**Updated:**` timestamp descending. Ask: "Какую инициативу продолжить? [1/2/...]"
After selection → show **Summary** + **Stale Check**.

## Summary Format

```
┌────────────────────────────────────────┐
│ Resume: {INIT-ID}                      │
├────────────────────────────────────────┤
│ Profile: {profile}                     │
│ Phase:   {phase}                       │
│ Last:    {last_command} ({date})        │
│ Next:    {next_command}                 │
│                                        │
│ Decisions ({count}):                   │
│ • {decision_1}                         │
│ • {decision_2}                         │
│                                        │
│ Open questions ({count}):              │
│ • {question_1}                         │
│                                        │
│ {stale_status}                         │
└────────────────────────────────────────┘
```

## Stale Check

For each file listed in session's "Context Files" section:
1. Check if file exists — if not, warn: "⚠️ {file} не найден — возможно переименован"
2. Compare file modification time against session's `**Updated:**` timestamp
3. If file is newer → warn: "⚠️ {file} изменён после последней сессии. Resync? [Y/N]"
4. If resync → re-read the stale artifact, update session's Context Files section, update timestamp

If no stale files: "✅ Артефакты актуальны"

## Rules
- This command does NOT advance the lifecycle — it is a reader/presenter only
- Do NOT auto-execute the next command — always ask for user confirmation
- Parse session files tolerantly — if format is corrupted, warn and suggest re-creating via next `/speckit-*` command
- If session file is > 50 lines, truncate Decisions to last 5 when displaying
