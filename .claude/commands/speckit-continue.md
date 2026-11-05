---
description: Resume from last checkpoint or show multi-initiative dashboard
argument-hint: [INIT-YYYY-NNN-slug] (optional)
---

You are helping the user resume work on a SpecKit initiative.

## Your job

1. **Discover sessions:** Glob `.specify/session/INIT-*.md` (skip TEMPLATE.md, protocol.md).

2. **Route by case:**

Session files are local and not committed, so a missing session does not mean the work has not started. Without a session, compute the state from the files with `speckit-status.py`.

### Case A: No argument, no sessions found
1. Glob `initiatives/INIT-*/` (skip directories with `{` in the name).
2. If there are none, say: "Инициатив пока нет. Запустить `/speckit-start`?" Stop.
3. Otherwise run `python3 tools/scripts/speckit-status.py {INIT-ID} --json` for each and show the **Dashboard** with phase = `next.id` and next = `next.command`. Ask which one to continue. After selection, show the **Status Summary**.

### Case B: INIT-ID provided in $ARGUMENTS
1. Read `.specify/session/$ARGUMENTS.md`
2. If not found → run `python3 tools/scripts/speckit-status.py $ARGUMENTS --json`:
   - if `diagnostics` has an item with `severity: error`, show its `message` and `fix`. Stop.
   - otherwise show the **Status Summary** and propose `next.command`.
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

## Status Summary

Used when there is no session file. It has no decisions or open questions: those live only in sessions.

```
Статус: {initiative} (из файлов, сессии нет)
Профиль: {profile}

Готово:   {ids of steps with state done}
Пропущено: {ids of steps with state skipped, omit the line if none}
Следом:   {next.command}
Заблокировано: {ids of steps with state blocked}

{each diagnostic: severity, message, fix}
```

If `next.also_consider` is not empty, mention it before the graduation. If `next` is null and `steps` is not empty, say that all steps are done.

## Stale Check

For each file listed in session's "Context Files" section:
1. Check if file exists — if not, warn: "⚠️ {file} не найден — возможно переименован"
2. Compare file modification time against session's `**Updated:**` timestamp
3. If file is newer → warn: "⚠️ {file} изменён после последней сессии. Resync? [Y/N]"
4. If resync → re-read the stale artifact, update session's Context Files section, update timestamp

If no stale files: "✅ Артефакты актуальны"

## Rules
- This command does NOT advance the lifecycle — it is a reader/presenter only
- `speckit-status.py` judges by files: a step counts as done when its artifact exists and is filled, not when someone checked its content
- Do NOT auto-execute the next command — always ask for user confirmation
- Parse session files tolerantly — if format is corrupted, warn and suggest re-creating via next `/speckit-*` command
- If session file is > 50 lines, truncate Decisions to last 5 when displaying
