---
description: Update domain artifacts — add glossary terms, canonical model entities, or events
argument-hint: <domain-name> (e.g., auth, billing, inventory)
---

You are updating the domain specification for `$ARGUMENTS`.

## Your job

1. Read `domains/$ARGUMENTS/glossary.md`.
2. Read `domains/$ARGUMENTS/canonical-model.md`.
3. Read `domains/$ARGUMENTS/event-catalog.md`.
4. Scan other `domains/*/glossary.md` files to check for term conflicts.

5. Ask the user what they want to update:
   - [ ] Add / update a **glossary term**
   - [ ] Add / update a **canonical model entity or relationship**
   - [ ] Add / update a **domain event**
   - [ ] Update **NFR** constraints

6. **For each update type, collect:**

   **Glossary term:**
   - Term name (canonical, PascalCase)
   - Business definition (what it IS — no implementation details)
   - Synonyms used informally
   - What it is NOT (disambiguate from similar terms)
   - Where it is used (products, initiatives)

   **Canonical model entity:**
   - Entity name
   - Identity attribute(s)
   - Key business attributes
   - Invariants (business rules that must always hold)
   - Relationships to existing entities
   - Lifecycle states

   **Domain event:**
   - Event name (must follow `<domain>.<entity>.<past-tense-verb>`)
   - Business trigger (what user action or system event causes it)
   - Key payload fields
   - Downstream consumers
   - AsyncAPI channel reference

7. **Conflict detection:**
   - If adding a glossary term that already exists in another domain, flag:
     ```
     ⚠️ TERM CONFLICT: "<Term>" already defined in domains/billing/glossary.md
     Disambiguate: add "In <domain> context: ..." qualifier or use a distinct name
     ```
   - If adding an event with a name collision, flag and require rename.

8. Apply updates to the relevant file(s).

9. Report:
   - What was updated and in which file
   - Any conflicts found and how they were resolved
   - If an event was added: `Remember to add the channel to contracts/asyncapi.yaml in the relevant initiative`

## Rules
- Term definitions MUST be in business language — no code types, no DB column names
- Event names MUST be unique across ALL domains — scan all `event-catalog.md` files before adding
- Updating an existing entity MUST NOT remove existing invariants without user confirmation
- Mark deprecated terms with `**Deprecated:** <date> — use <NewTerm> instead` rather than deleting

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS or context | **Type:** utility | **Next:** _(preserve current)_
