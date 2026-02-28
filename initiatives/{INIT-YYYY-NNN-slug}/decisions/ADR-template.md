---
status: "proposed"
date: "{YYYY-MM-DD}"
decision-makers: ["@{techlead}", "@{architect}"]
consulted: ["@{security}", "@{sre}"]
informed: ["@{product}", "@{support}"]
---

# {INIT}-ADR-{NNN}: {Короткий заголовок решения}

## Context and problem statement

{Что происходит, какая боль/ограничение, какие требования/архитектурные драйверы (ASR)}

## Decision drivers

- {driver 1: требование / ограничение / качественный атрибут}
- {driver 2}

## Considered options

- **Option A:** {кратко}
- **Option B:** {кратко}
- **Option C:** {кратко}

## Decision outcome

**Chosen option:** "{A|B|C}", because {рационал, trade-offs относительно decision drivers}.

### Consequences

- **Good:** {…}
- **Bad:** {…}
- **Neutral:** {…}

### Confirmation

{Как мы проверим, что решение «работает»: тест / метрика / ревью / инцидент-порог}

---

*Шаблон основан на [MADR](https://adr.github.io/madr/) (включая YAML front-matter и Confirmation).*
