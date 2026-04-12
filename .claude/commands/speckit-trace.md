---
description: Generate or update trace.md (RTM) for a feature spec, then verify with make check-trace
argument-hint: <NNN>-<slug> (e.g., 001-user-auth)
---

**Context loading:** Before step 1, check if `.specify/session/{INIT-ID}.md` exists (where INIT-ID = $ARGUMENTS). If found, read session file and load only "Context Files" per phase table in `.specify/session/protocol.md`. If `--full-context` passed, load all files. If no session found, proceed as below.

You are building the Requirements Traceability Matrix for `.specify/specs/$ARGUMENTS/`.

## Your job

1. Read `.specify/specs/$ARGUMENTS/spec.md` — collect all REQ-IDs referenced.
2. Read `.specify/specs/$ARGUMENTS/plan.md` — extract ADR references and contract paths.
3. Read the parent initiative's `requirements.yml` — get the full list of REQ-IDs:
   - Initiative ID is in `spec.md` **Initiative:** field.
4. Read the initiative's `contracts/openapi.yaml` and `contracts/asyncapi.yaml` — map paths/channels.
5. Scan test files referenced in `requirements.yml` trace sections.

6. Build the traceability table for `.specify/specs/$ARGUMENTS/trace.md`:

   ```markdown
   # Traceability: $ARGUMENTS

   | REQ-ID | ADR | Contract | Schema | Tests | SLO |
   |---|---|---|---|---|---|
   | `REQ-XXX-001` | `decisions/INIT-…-ADR-0001-slug.md` | `contracts/openapi.yaml#/paths/~1resource/post` | `contracts/schemas/resource.schema.json` | `tests/api/resource.spec.ts::REQ-XXX-001` | — |
   ```

   Rules per cell:
   - **ADR**: link if plan.md references a decision for this REQ; otherwise `—`
   - **Contract**: OpenAPI `#/paths/...` or AsyncAPI `#/channels/...` anchor; `—` if no contract
   - **Schema**: JSON Schema file path; `—` if no dedicated schema
   - **Tests**: `tests/path/file.spec.ts::REQ-XXX-NNN` format; `—` if not yet written
   - **SLO**: `ops/slo.yaml#<slo-id>`; only for `nfr` type requirements; `—` otherwise

7. Flag any REQ-ID where ALL cells except REQ-ID are `—`:
   ```
   ⚠️  GAP: REQ-XXX-002 has no traceability links (no contract, no test, no SLO)
   ```
   These are blockers for Standard/Extended profile DoD.

8. **Sync trace links back to requirements.yml**: For each REQ-ID in trace.md, update the corresponding `trace:` section in `initiatives/{INIT}/requirements.yml` with:
   - `adr:` links (if ADR column is non-`—`)
   - `contracts:` links (if Contract column is non-`—`)
   - `schemas:` links (if Schema column is non-`—`)
   - `slo:` link (if SLO column is non-`—`)
   Then run `make validate` to confirm requirements.yml is still schema-valid.

9. Run check:
   ```
   make check-trace
   ```
   Fix any REQ-ID mismatches reported.

9. Report:
   - Total REQ-IDs traced
   - Count with full coverage (≥1 non-`—` cell)
   - GAPs list with recommended next actions

## Rules
- Every REQ-ID in `spec.md` MUST appear in `trace.md`
- A REQ-ID with all `—` links MUST NOT be marked as `implemented` in `requirements.yml`
- `make check-trace` MUST pass with zero errors before reporting success
- Do NOT fabricate test file paths — only link tests that actually exist
- For Standard/Extended profile: every REQ-ID MUST have ≥1 trace link

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS | **Type:** lifecycle | **Next:** /speckit-rtm
