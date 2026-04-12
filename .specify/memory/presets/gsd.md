# Preset: GSD-интеграция

> Опциональный execution engine для L4-фазы реализации. Встраивается только в L4.
> Загружается: speckit-gsd-bridge, speckit-gsd-verify, speckit-gsd-map, speckit-implement (GSD mode).
> Source: extracted from constitution.md v1.0.0

---

## Когда использовать

| Сценарий | Подход |
|---|---|
| Простая фича, 1 инженер, < 1 дня | `/speckit-implement` (линейно, T1→T6 по одному) |
| Сложная фича, несколько файлов, > 1 дня | `/speckit-gsd-bridge` → `/gsd-execute-phase` (wave-параллелизация) |
| Brownfield, незнакомая кодовая база | `/speckit-gsd-map` перед spec-циклом |
| Любая фича, где важна свежесть контекста | GSD (fresh context per subagent) |

## Permission boundaries

**GSD-субагенты** (агенты, порождаемые `/gsd-execute-phase`):
- MUST NOT модифицировать артефакты L0–L3 (`constitution.md`, `domains/`, `products/`, `initiatives/`)
- MAY модифицировать только implementation/test файлы и L4-артефакты (`.specify/specs/`)
- MUST NOT использовать `--dangerously-skip-permissions` — только granular permissions

**Spec Kit команды-оркестраторы** (`/speckit-gsd-bridge`, `/speckit-gsd-verify`, `/speckit-gsd-map`):
- Работают на уровне доверия пользователя, не являются GSD-субагентами
- `/speckit-gsd-map` MAY дополнять L2-артефакты (`products/*/architecture/`) с маркерами `[GSD-MAPPED]`
- `/speckit-gsd-verify` MAY писать в `evidence/` (L5)
- `/speckit-gsd-bridge` пишет только в `.planning/`

**Общие:**
- `STATE.md` и `SUMMARY.md` живут в `.planning/` — отдельно от `requirements.yml` и `trace.md`

## Артефакт-flow

```text
L4 tasks.md ──[/speckit-gsd-bridge]──> .planning/phases/SPEC-NNN/PLAN.md
                                            │
                                       [/gsd-execute-phase]
                                            │
                                            v
                                .planning/phases/SPEC-NNN/SUMMARY.md
                                            │
                                       [/speckit-gsd-verify]
                                            │
                                            v
                                     evidence/SPEC-NNN-verification.md
```

## Разделение ответственности

| Артефакт | Владелец | Назначение |
|---|---|---|
| `requirements.yml` | Spec Kit (L3) | Каноническая спецификация требований |
| `STATE.md` | GSD | Оперативная память сессии (блокеры, решения, позиция) |
| `SUMMARY.md` | GSD | Результат выполнения плана (что сделано, какие файлы) |
| `evidence/*.md` | Spec Kit (L5) | Верификация покрытия требований |
