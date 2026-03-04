---
description: Create a Product ADR in MADR format via guided questions
argument-hint: <product-name> (e.g., platform, analytics)
---

You are recording an Architecture Decision Record for product `$ARGUMENTS`.

## Your job

1. Read `products/$ARGUMENTS/decisions/` — find the highest existing ADR number to determine the next `NNNN`.
   If `decisions/` is empty, start at `0001`.
2. Read `products/$ARGUMENTS/architecture.md` for existing decisions context.
3. Read `.specify/memory/constitution.md` for ADR naming scheme: `$ARGUMENTS-NNNN-<slug>`.

4. Ask the user **5 questions** to capture the decision context:
   - **What decision needs to be made?** (1–2 sentences — the architectural question)
   - **Why now?** (driving force: requirement, incident, performance issue, new technology)
   - **What options were considered?** (at least 2; ask user to name them)
   - **What are the pros/cons of each option?**
   - **Which option is chosen and why?** (rationale + trade-offs accepted)

5. Ask for the decision slug: `<short-hyphenated-description>` (e.g., `cache-strategy`, `auth-provider`).
   Generate filename: `products/$ARGUMENTS/decisions/$ARGUMENTS-<NNNN>-<slug>.md`

6. Write the ADR in MADR format:
   ```markdown
   # $ARGUMENTS-<NNNN>: <Decision Title>

   **Status:** Accepted
   **Date:** <YYYY-MM-DD>
   **Deciders:** {placeholder: @handle, @handle}

   ## Context and Problem Statement

   <What is the architectural question? What forces are at play?>

   ## Decision Drivers

   - <driver 1: requirement, constraint, quality goal>
   - <driver 2>

   ## Considered Options

   - Option A: <name>
   - Option B: <name>
   - Option C: <name> (if applicable)

   ## Decision Outcome

   **Chosen option:** Option X — <rationale in 1–2 sentences>

   ### Positive Consequences
   - <pro 1>
   - <pro 2>

   ### Negative Consequences (trade-offs accepted)
   - <con 1>
   - <con 2>

   ## Pros and Cons of Options

   ### Option A: <name>
   - ✅ <pro>
   - ❌ <con>

   ### Option B: <name>
   - ✅ <pro>
   - ❌ <con>

   ## Links
   - Supersedes: — (or link to previous ADR)
   - Related REQ-IDs: {placeholder: REQ-XXX-NNN}
   ```

7. Update `products/$ARGUMENTS/architecture.md` — add reference to the new ADR in section 9.

8. Report:
   - ADR file created at `products/$ARGUMENTS/decisions/<filename>`
   - Remind user: `Link this ADR in requirements.yml trace.adr for related REQ-IDs`

## Rules
- Status MUST be `Accepted` at creation — if still in discussion, use `Proposed` and note open questions
- At least 2 options MUST be documented — single-option ADRs are not allowed
- ADR filename MUST match scheme: `<product>-NNNN-<slug>.md` (zero-padded, lowercase slug)
- Do NOT alter existing ADRs — create a new one that supersedes if a decision changes
- Related REQ-IDs MUST be listed in the Links section
