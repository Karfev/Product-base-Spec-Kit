# Changelog

Версии самого фреймворка. Формат: [Keep a Changelog](https://keepachangelog.com/). Версионирование: [SemVer](https://semver.org/). Текущая версия указана в файле `VERSION`, тег релиза — `kit-vX.Y.Z`.

Как читать номер версии:

- **Major:** форку нужна миграция данных или изменились обязательные правила конституции.
- **Minor:** новые команды, проверки и поля, существующие данные остаются валидными.
- **Patch:** исправления без изменения правил.

Как обновить форк: `tools/kit-update.sh <remote-или-путь> <тег>`, см. [PLAT-0006](decisions/PLAT-0006-kit-versioning-and-updates.md).

## [1.0.0] — 2026-11-05

Первая версия с номером. Форкам, созданным раньше, нужно свериться с разделом «Изменено несовместимо».

### Добавлено

- `tools/scripts/graduate.py`: слияние требований, ADR и журнала знаний в продукт кодом, с тестами.
- `tools/scripts/check-deltas.py` и `make check-deltas`: конфликты требований с реестром продукта до слияния.
- Поля требований `delta`, `base_rev`, `removal_reason`: изменённое требование сохраняет свой REQ-ID.
- `check-trace --strict` и внешние ссылки на тесты `ext:<repo>/<path>::REQ-ID`.
- `tools/scripts/speckit-status.py` и `make status`: состояние инициативы, вычисленное из файлов.
- `tools/kit-update.sh`, `tools/kit-paths.txt`, `VERSION`: обновление форка из тега.
- `make test-tools`, `make test-lifecycle` и CI-job'ы для чистого клона и полного цикла инициативы.

### Изменено несовместимо

- Конституция 3.0.0: текущее поведение продукта описывает `requirements-registry.yml`, а `requirements.yml` инициативы — предлагаемое изменение.
- `requirements-registry.yml` перешёл на `schema_version: 2`. Реестр старого формата отклоняется, см. [PLAT-0005](decisions/PLAT-0005-requirements-delta-model.md).
- `check-trace` стал блокирующим для `implemented` и `verified`: битая ссылка или пустое подтверждение — ошибка. Для остальных статусов это предупреждения.
- `check-trace` требует строку в `trace.md` своей инициативы: чужая строка больше не засчитывается.

### Изменено

- `/speckit-graduate` сокращён до диалога вокруг `graduate.py`. Слияние контрактов пока остаётся в промпте.
- `/speckit-continue` показывает состояние из файлов, если файла сессии нет.
- `make install-tools` работает без глобальных инструментов.

### Исправлено

- `tools/archive.sh` и `tools/restore.sh` работают на Linux.
