# Spec: 010-ai-quality-gates

**Initiative:** INIT-2026-007-quality-augmentation
**Profile:** Minimal
**Owner:** @dmitriy
**Last updated:** 2026-04-12

## Summary

Кодифицированные AI quality constraints для implementation phase: `tools/ai-quality-gates.md` + enforcement checklist в `/speckit-implement` + CI lint в `check-spec-quality.py`.

## Motivation / Problem

SpecKit's T1-T6 задаёт порядок (contracts → tests → code → integration → observability → trace), но не содержит quality constraints для самого кода. Агент может написать 300-строчный метод, пропустить stubs, начать с T2b вместо T2a. Качество зависит от "настроения" модели.

Datarim кодифицирует это через Five Pillars of AI Quality: decomposition (max 50 LOC), TDD enforcement, architecture-first, focused work, context management. Результат: за 1000+ задач — стабильное качество без деградации.

SpecKit нужна своя версия, адаптированная под spec-first + contract-aware подход.

## Scope

- REQ-QUAL-004: AI quality gates document
- REQ-QUAL-005: Enforcement checklist в `/speckit-implement`

## Non-goals

- Runtime code analysis (linting, static analysis) — вне scope
- Автоматическое refactoring — только предупреждения
- Модификация JSON Schemas или constitution.md
- Quality gates для Minimal профиля (только Standard+)

## User stories

- As a developer using `/speckit-implement`, I want clear quality constraints before I start coding, so that I produce consistent output regardless of session context.
- As a tech lead, I want CI to catch when tests are written after code (T2b before T2a), so that TDD discipline is enforced at pipeline level.
- As an architect, I want implementation to match contract signatures, so that OpenAPI/AsyncAPI specs are the source of truth.

## AI Quality Gates (Five Pillars, SpecKit Edition)

### Pillar 1: Decomposition

```
RULES:
- Max 50 LOC per method/function (excluding comments and blank lines)
- Max 7-9 objects/entities in active scope per task
- Single Responsibility: one function = one job
- If method > 50 LOC → decompose before proceeding

ENFORCEMENT:
- /speckit-implement prompts: "Метод {name} = {N} строк. Decompose?"
```

### Pillar 2: Test-First (TDD)

```
RULES:
- T2a MUST complete before T2b starts
- Tests define the interface: write test → derive function signature → implement
- Arrange-Act-Assert pattern for unit tests
- Contract tests validate OpenAPI/AsyncAPI compliance

ENFORCEMENT:
- /speckit-implement blocks T2b if T2a not marked done in tasks.md
- check-spec-quality.py: T2b before T2a → CI warning
```

### Pillar 3: Architecture-First

```
RULES:
- Create skeleton stubs (interfaces, type signatures, empty handlers) before implementation
- Get stubs reviewed/approved before filling in logic
- Implement one method at a time, not entire module
- Stubs MUST match contract signatures (OpenAPI paths, AsyncAPI handlers)

ENFORCEMENT:
- /speckit-implement asks: "Stubs created and match contracts? [Y/N]"
```

### Pillar 4: Focused Work

```
RULES:
- One task = one bounded context (single handler, single endpoint, single event)
- Explicit scope boundaries before each T2b: "This task covers: <files>, <methods>"
- No side-effect changes outside declared scope

ENFORCEMENT:
- /speckit-implement prompts: "Scope for this task: <declared scope>. Proceed? [Y/N]"
```

### Pillar 5: Contract-Aware (SpecKit-specific)

```
RULES:
- Implementation MUST match contract signatures:
  - REST: HTTP method + path + request/response schemas from OpenAPI
  - Events: channel + message schema from AsyncAPI
  - Data: entity schemas from contracts/schemas/*.json
- Contract validation: make lint-contracts MUST pass before T2b
- Breaking changes: require ADR + deprecation plan

ENFORCEMENT:
- /speckit-implement runs make lint-contracts before T2b
- Mismatch → blocker with specific diff
```

## CI Extension

### check-spec-quality.py additions

```python
# New rule: T2b-before-T2a detection
def check_task_ordering(tasks_md_path):
    """
    Parse tasks.md, verify T2a checkbox is checked
    before T2b checkbox is checked.
    
    - If T2b checked and T2a not checked → WARNING
    - If both unchecked → OK (not started)
    - If T2a checked and T2b not checked → OK (in progress)
    """
    
# New rule: quality gates reference
def check_quality_gates_reference(spec_path):
    """
    For Standard+ specs, verify tasks.md references
    tools/ai-quality-gates.md in header or imports.
    
    - If not referenced → INFO (soft suggestion)
    """
```

## Requirements

- REQ-QUAL-004 (P1): AI quality gates document
- REQ-QUAL-005 (P1): Enforcement checklist в `/speckit-implement`

## Acceptance criteria

- Given `tools/ai-quality-gates.md` exists, when `/speckit-implement` reads it, then 5 pillars loaded as checklist
- Given T2a not done, when `/speckit-implement` attempts T2b, then warning "T2a incomplete — write tests first"
- Given method > 50 LOC generated, when agent reviews output, then prompt to decompose
- Given contract mismatch (OpenAPI path missing handler), when T2b starts, then blocker with specific diff
- Given tasks.md with T2b checked before T2a, when `make check-spec-quality`, then CI warning emitted

## Open Questions

| # | Question | Owner | Deadline | Status |
|---|----------|-------|----------|--------|
| 1 | Включать ли LOC counting как CI lint (static analysis) или только как agent prompt? | @dmitriy | 2026-04-25 | open |
| 2 | Применять ли quality gates к Minimal профилю (currently excluded)? | @dmitriy | 2026-04-25 | open |
