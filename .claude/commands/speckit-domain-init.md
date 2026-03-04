---
description: Scaffold a new domain spec folder with glossary, canonical model, event catalog, and NFR
argument-hint: <domain-name> (e.g., auth, billing, inventory)
---

You are initializing the domain-level specification for `$ARGUMENTS`.

## Your job

1. Check if `domains/$ARGUMENTS/` already exists — if so, ask to update or abort.
2. Read `domains/README.md` for the expected structure.
3. Read `.specify/memory/constitution.md` for L1 requirements.

4. Ask the user:
   - What is the domain's core business responsibility? (1–2 sentences, no jargon)
   - Who is the domain owner? (`@handle` or team name)
   - Which bounded context does this cover? (DDD perspective)
   - Are there adjacent domains to cross-reference?

5. Create `domains/$ARGUMENTS/` with:

   **`glossary.md`**:
   ```markdown
   # Glossary: $ARGUMENTS domain
   Owner: @<handle> | Updated: <date>

   Terms in this domain. Adjacent domains: {placeholder: links to domains/<name>/glossary.md}

   ## Terms

   ### <Term Name>
   **Definition:** {placeholder: precise business definition — what it IS}
   **Synonyms:** {placeholder: alternative names used informally}
   **Distinguishes from:** {placeholder: what it is NOT — anti-ambiguity}
   **Used in:** {placeholder: products, initiatives that use this term}
   ```

   **`canonical-model.md`**:
   ```markdown
   # Canonical Model: $ARGUMENTS domain
   Owner: @<handle> | Updated: <date>

   Core business objects and their relationships.

   ## Entities

   ### <EntityName>
   **Identity:** {placeholder: what uniquely identifies this entity}
   **Key attributes:** {placeholder: business-relevant fields — NOT implementation schema}
   **Invariants:** {placeholder: business rules that must always hold}
   **Relationships:** {placeholder: associations to other entities}
   **Lifecycle:** {placeholder: states and transitions}

   ## Value Objects
   {placeholder: immutable objects with no identity}

   ## Aggregates
   {placeholder: consistency boundaries and roots}
   ```

   **`event-catalog.md`**:
   ```markdown
   # Event Catalog: $ARGUMENTS domain
   Owner: @<handle> | Updated: <date>

   Domain events published by this bounded context.

   ## Events

   ### <domain>.<entity>.<past-tense-verb>
   **Description:** {placeholder: what happened in business terms}
   **Trigger:** {placeholder: what business action caused this event}
   **Payload (key fields):** {placeholder: entity ID + changed attributes}
   **Consumers:** {placeholder: which products/services react to this event}
   **Channel:** {placeholder: asyncapi channel name}
   ```

   **`nfr.md`**:
   ```markdown
   # NFR: $ARGUMENTS domain
   Owner: @<handle> | Updated: <date>

   Non-functional constraints for all services in this domain.

   ## Data Classification
   {placeholder: PII / financial / regulated / internal / public}

   ## Compliance
   {placeholder: GDPR, SOC2, HIPAA, PCI-DSS applicability}

   ## Cross-cutting Security
   {placeholder: required auth mechanisms, encryption standards}
   ```

   **`README.md`**:
   ```markdown
   # $ARGUMENTS domain
   <one-line business responsibility>
   Owner: @<handle>

   - Glossary: `glossary.md`
   - Canonical model: `canonical-model.md`
   - Event catalog: `event-catalog.md`
   - Domain NFR: `nfr.md`
   - Products in this domain: {placeholder: `products/<name>/`}
   ```

6. Report all created files and next steps:
   - `Fill glossary.md with business terms before any L3 initiative in this domain`
   - `Run /speckit-domain-update $ARGUMENTS to add terms, events, or update the model`

## Rules
- Canonical model MUST use business language — no SQL schemas, no JSON structures
- Glossary terms MUST distinguish from similar terms in adjacent domains
- Event names MUST follow pattern: `<domain>.<entity>.<past-tense-verb>` (e.g., `auth.api-key.created`)
- Do NOT invent business rules — ask the user for each invariant
