# Migration Plan: INIT-2026-002-notification-preferences

**Профиль:** Extended
**Последнее обновление:** 2026-04-10

## Тип миграции

- [ ] Schema migration (БД)
- [ ] Data migration (данные)
- [ ] Contract migration (breaking change)
- [ ] Infrastructure migration

## Предусловия

- {Условие 1 перед запуском миграции}
- {Условие 2}

## Шаги миграции

| Шаг | Описание | Обратимый? | Команда / скрипт |
|---|---|---|---|
| 1 | {Добавить новый столбец (nullable)} | Да | `migrations/V{N}__add_{column}.sql` |
| 2 | {Заполнить данные} | Да | `scripts/migrate-data.sh` |
| 3 | {Сделать NOT NULL} | **Нет** | `migrations/V{N+1}__set_notnull.sql` |

## Rollback

| Шаг | Rollback-команда |
|---|---|
| 1 | `migrations/V{N}__rollback.sql` |
| 2 | Данные неизменны |
| 3 | ⚠️ Необратимо — откат через новую миграцию |

## Валидация после миграции

```bash
# {Команда проверки}
{validation-script.sh}
```

Ожидаемый результат: {описание}
