---
description: Multi-perspective ADR review — generate domain evaluations from Архкомм-aligned roles
argument-hint: <path-to-ADR> [--preset standard|archkom-l1|archkom-l2] [--roles "role1,role2"]
---

You are running a structured multi-perspective review of an ADR (Architecture Decision Record).

## Your job

1. **Parse arguments.**
   - `$ARGUMENTS` contains: `<adr_path>` and optional flags `--preset <name>` or `--roles "<comma-separated>"`.
   - If no ADR path provided, ask: "Укажи путь к ADR файлу (e.g., products/platform/decisions/PLAT-0003-async-queue.md)"

2. **Read the ADR file.** Parse its content completely.

3. **Read role definitions.**
   Read `.specify/memory/consilium-roles.yml` — load `roles`, `presets`, and `profile_defaults`.

4. **Determine panel composition (REQ-QUAL-002, REQ-QUAL-006):**

   **Priority order:**
   a. If `--roles` flag provided → parse comma-separated role IDs, match against `roles[].id` in consilium-roles.yml. Error if any ID not found.
   b. If `--preset` flag provided → load preset from `presets` section. Error if preset not found.
   c. If neither flag → auto-detect from initiative profile:
      - Read the initiative's `requirements.yml` metadata to get `profile`
      - Map profile to preset using `profile_defaults` in consilium-roles.yml
      - If profile = `minimal` or mapping is `null` → inform user: "Consilium не применяется к Minimal профилю. Используйте `--preset standard` для принудительного запуска." Stop.

   Announce: "Panel: {N} ролей ({role names}). Preset: {preset_name|custom}."

5. **Execute sequential role reviews (REQ-QUAL-001).**

   For each role in the panel:

   a. **Load context files.** For each path in `role.context_files`:
      - Replace `{product}` with the product from initiative metadata (or ask user)
      - Replace `{domain}` with the domain from initiative metadata (or infer from ADR path)
      - If the file exists → read it (extract relevant sections, max 500 tokens per file)
      - If the file doesn't exist → note: "Артефакт {path} не найден — пропускаем этот контекст"

   b. **Analyze the ADR** from this role's perspective using the checklist:

      For each checklist item:
      1. Check if the item is covered in the ADR
      2. If covered adequately → **OK** with brief confirmation
      3. If covered but with concerns → **Замечание** with specific observation and artifact reference
      4. If critical gap → **Блокер** with specific description of what's missing

   c. **Generate role output** in this format:
      ```
      ### {role.name}

      | Пункт | Статус | Комментарий |
      |---|---|---|
      | {checklist_item_1} | OK / Замечание / Блокер | {specific detail with artifact reference} |
      | {checklist_item_2} | ... | ... |

      **Итог:** {OK / Замечание / Блокер} — {one-sentence summary}
      ```

6. **Aggregate results (REQ-QUAL-003).**

   Build the "Доменные оценки" section:

   ```markdown
   ## Доменные оценки (consilium)

   > Сгенерировано `/speckit-consilium` {today's date}. Preset: {preset_name}.

   | Домен | Статус | Комментарий |
   |---|---|---|
   | {role_1.name} | {verdict} | {summary} |
   | {role_2.name} | {verdict} | {summary} |
   | ... | ... | ... |

   **Итог:** {overall_verdict}
   ```

   Overall verdict logic:
   - Any **Блокер** → "Требует доработки"
   - Only **Замечания** (no Блокеры) → "Одобрено с условиями"
   - All **OK** → "Одобрено"

   If overall = "Требует доработки" or "Одобрено с условиями", add conditions table:
   ```markdown
   **Условия:**

   | # | Условие | Источник | Приоритет |
   |---|---------|----------|-----------|
   | 1 | {specific action required} | {role_name} | Блокер / Замечание |
   ```

7. **Inject section into ADR.**

   - Check if ADR already has a `## Доменные оценки` section
   - If yes → **replace** the existing section (from `## Доменные оценки` to the next `## ` heading or end of file)
   - If no → **append** the section before the last heading or at the end of the file

8. **Print summary to console.**

   ```
   Consilium review complete for {adr_filename}

   Panel: {N} roles ({preset_name})
   | Домен | Статус |
   |---|---|
   | {role_name} | {verdict} |

   Overall: {overall_verdict}
   {If blockers: "Blockers: N — resolve before Архкомм submission"}
   ```

## Rules
- NEVER auto-approve — consilium generates review, human decides
- Each role MUST reference specific artifacts or ADR sections in findings — no vague "looks good"
- If context file doesn't exist, role still runs but notes the missing context
- Checklist items without clear evidence in ADR → default to "Замечание" (not OK)
- For Standard+ profile only — Minimal initiatives skip consilium
- Maximum context per role: 500 tokens per file, 3 files max (prevent context overflow)
- Output format MUST be compatible with ADR-template-v2 "Доменные оценки" section
