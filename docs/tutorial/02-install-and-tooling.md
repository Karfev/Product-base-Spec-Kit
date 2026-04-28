# 02. Установка и tooling

> **Аудитория:** Dev / Tech Lead.
> **Время:** 10–15 минут.
> **Предыдущий:** [01-glossary.md](./01-glossary.md) | **Следующий:** [03-first-initiative.md](./03-first-initiative.md)

---

## TL;DR

```bash
# 1. Системные зависимости (Python 3.10+, Node 18+, git)
# 2. Клонировать репо
git clone https://github.com/Karfev/Product-base-Spec-Kit.git
cd Product-base-Spec-Kit

# 3. Установить tooling
make install-tools

# 4. Проверить
make help
make validate
```

Если все три команды отработали без ошибок — можно переходить к [03-first-initiative.md](./03-first-initiative.md).

---

## Что нужно поставить заранее

| Компонент | Минимальная версия | Зачем |
|---|---|---|
| **Python** | 3.10 | `pyyaml`, `check-jsonschema` (валидация YAML против JSON Schema) |
| **Node.js** | 18 | `markdownlint-cli2`, `redocly`, `asyncapi` (lint контрактов) |
| **git** | любая современная | clone, PR-workflow |
| **make** | GNU make 3.81+ (на macOS — встроен; Windows — см. ниже) | task runner |
| **AI-агент** (опционально) | Claude Code / OpenCode / Kilo Code | для `/speckit-*` команд |

## Платформа за платформой

### macOS

```bash
# Если Python/Node не установлены:
brew install python@3.12 node@20

# Проверка
python3 --version   # должно быть 3.10+
node --version      # должно быть v18+
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip nodejs npm make git

python3 --version
node --version
```

### Windows (через WSL2)

Нативный Windows работает плохо — `make`, bash-скрипты в `tools/`, JSON Pointer-paths
с экранированием `~1` для `/` ломаются в PowerShell.

**Рекомендация:** WSL2 + Ubuntu.

```powershell
# В PowerShell (admin):
wsl --install -d Ubuntu

# Перезагрузка, затем внутри WSL:
sudo apt-get update
sudo apt-get install -y python3 python3-pip nodejs npm make git
```

Дальше всё как в Linux.

---

## Установка tooling репозитория

После клонирования:

```bash
make install-tools
```

Эта цель ставит:

| Пакет | Источник | Зачем |
|---|---|---|
| `pyyaml` | pip | parser YAML для скриптов в `tools/scripts/` |
| `check-jsonschema` | pip | валидация `requirements.yml` против JSON Schema |
| `markdownlint-cli2` | npm (-g) | проверка `.md` файлов |
| `@redocly/cli` | npm (-g) | lint OpenAPI |
| `@asyncapi/cli` | npm (-g) | validate AsyncAPI |

> **💡 Если pip ругается на externally-managed environment** (Ubuntu 23.04+, macOS):
> добавь флаг `--break-system-packages` или используй `pipx`. Альтернатива —
> `python3 -m venv .venv && source .venv/bin/activate && make install-tools`.

### `oasdiff` отдельно

`oasdiff` (детектор breaking changes в OpenAPI) — Go-бинарник, не устанавливается через
`make install-tools`. Если планируешь работать с контрактами:

```bash
# macOS / Linux
brew tap oasdiff/oasdiff
brew install oasdiff
# или
go install github.com/oasdiff/oasdiff@latest
```

Без `oasdiff` локально CI всё равно отработает — он живёт в GitHub Actions.

---

## Проверка установки

```bash
# 1. make-цели должны показаться
make help

# Ожидаемый вывод (фрагмент):
#   help                 Show available commands
#   validate             Validate all active requirements.yml...
#   check-trace          Check REQ-ID consistency (L3 <-> L4)
#   ...

# 2. Валидация существующих инициатив (должно пройти)
make validate

# Ожидаемый вывод:
# ==> Validating requirements.yml files...
#   Checking initiatives/INIT-2026-000-api-key-management/requirements.yml
#   ...

# 3. (опционально) полный комплект
make check-all
```

Если `make validate` зелёный — окружение готово.

---

## Опциональное: настройка AI-агента

Touториал можно проходить **без AI-агента** — все шаги работают через CLI и текстовый
редактор. Но `/speckit-*` команды экономят 60–80% рутины.

| Агент | Setup | Особенность |
|---|---|---|
| **Claude Code** | Built-in: открой репо, агент сам найдёт `.claude/commands/` | Native поддержка, рекомендуется для туториала |
| **OpenCode** | См. [`docs/SETUP-OPENCODE.md`](../SETUP-OPENCODE.md) | Поддержка локальных LLM (Ollama) |
| **Kilo Code** | См. [`docs/SETUP-KILOCODE.md`](../SETUP-KILOCODE.md) | VS Code / JetBrains plugin |

---

## Top-5 проблем при установке

| Симптом | Причина | Фикс |
|---|---|---|
| `python3: command not found` | Python не в PATH (Windows) | Используй WSL или установи Python через Microsoft Store |
| `error: externally-managed-environment` | pip 23+ блокирует системные установки | `pip install --break-system-packages` или venv |
| `make: command not found` (Windows native) | GNU make не входит в Windows | Используй WSL |
| `npm install -g` падает на permission | глобальная папка npm требует root | `sudo` или `npm config set prefix '~/.npm-global'` |
| `redocly: not found` после `make install-tools` | npm global bin не в PATH | `export PATH="$PATH:$(npm config get prefix)/bin"` в `.bashrc/.zshrc` |

Полный список — в [08-when-it-breaks.md](./08-when-it-breaks.md#установка).

---

## Проверка: можешь ли пройти первую инициативу

Минимальный sanity check перед переходом к [03-first-initiative.md](./03-first-initiative.md):

```bash
# Все три команды должны вернуть exit code 0
make help
make validate
python3 -c "import yaml, check_jsonschema; print('Python deps OK')"
```

Если первые две ✅ — двигайся дальше. Третья команда полезна, если что-то странное
происходит с pip/venv.

---

> **💡 Для тимлида.** При rollout в команду 5+ человек сделай скрипт `bootstrap.sh`
> (см. [09-team-rollout.md](./09-team-rollout.md#bootstrap-скрипт)) — это сэкономит
> 30+ минут на каждом новичке и уберёт «у меня не ставится».

---

**Дальше:** [03-first-initiative.md](./03-first-initiative.md) — создаём `INIT-2026-099-csv-export` с нуля за 30 минут.
