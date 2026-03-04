# services/

**L2.5 Service-уровень.** Каждая папка — одна услуга (единица сервисного каталога), порождённая конкретным Product (L2).

Услуга — это то, **что именно продукт предоставляет потребителю**: с SLA, тарификацией, поддержкой и порядком взаимодействия. Инициативы (L3) реализуют **изменения** в услугах.

```
products/{product}/   →   services/{service-code}/   →   initiatives/{INIT}/
     L2                          L2.5                           L3
```

---

## Как использовать

1. Скопировать `{service-code}/` → `<ваш-код-услуги>/` (например: `vtsod-vmwr-vs/`)
2. Заполнить все `{placeholder}` — начать с `README.md`
3. Выбрать профиль: **Minimal / Standard / Extended**
4. Удалить файлы профилей выше выбранного
5. Добавить ссылку на новую услугу в `products/{product}/README.md`

---

## Профили обязательности

Профиль выбирается **по степени критичности и клиентской видимости** услуги.

| Профиль | Обязательные файлы |
|---|---|
| **Minimal** | `README.md`, `external-spec.md`, `requirements.yml` |
| **Standard** | Minimal + `internal-spec.md`, `rsm.md`, `responsibilities.yml`, `ops/slo.yaml`, `ops/incident-catalog.yml`, `ops/request-catalog.yml` |
| **Extended** | Standard + `billing/parameters.yml`, `ops/change-catalog.yml`, `appendices/connection-guide.md`, `appendices/request-forms.md`, `appendices/report-templates.md` |

---

## Структура директории услуги

```
{service-code}/
├── README.md                     # Идентификатор, ссылки product ↑ и initiatives ↓
├── external-spec.md              # Клиентская спецификация (нарратив, → machine-readable якоря)
├── internal-spec.md              # Внутренняя спецификация доставки (нарратив)
├── rsm.md                        # Ресурсно-сервисная модель (Mermaid-диаграммы)
├── requirements.yml              # Machine-readable SLA/функциональные требования (REQ-SVC-*)
├── responsibilities.yml          # Матрица ответственности по архитектурным блокам
├── billing/
│   └── parameters.yml           # Тарифицируемые параметры, шаги и лимиты изменения
├── ops/
│   ├── slo.yaml                  # OpenSLO v1: доступность, SLI/SLO/Error Budget
│   ├── incident-catalog.yml      # Классификация инцидентов, пороги, SLT
│   ├── request-catalog.yml       # Каталог типовых запросов, приоритеты, SLT
│   └── change-catalog.yml        # Параметры стандартных/нестандартных изменений
└── appendices/
    ├── connection-guide.md       # Технические условия на подключение (Прил. А)
    ├── request-forms.md          # Формы типовых запросов (Прил. Б)
    └── report-templates.md       # Формы отчётов (Прил. В)
```

---

## Machine-readable якоря (Sources of Truth)

Narrative-файлы (`external-spec.md`, `internal-spec.md`) MUST ссылаться на якоря и НЕ дублировать их.

| Якорь | Файл | Схема |
|---|---|---|
| Тарифицируемые параметры | `billing/parameters.yml` | `tools/schemas/billing-parameters.schema.json` |
| Матрица ответственности | `responsibilities.yml` | `tools/schemas/responsibilities.schema.json` |
| SLO (доступность, задержки) | `ops/slo.yaml` | OpenSLO v1 |
| Каталог инцидентов | `ops/incident-catalog.yml` | `tools/schemas/incident-catalog.schema.json` |
| Каталог запросов | `ops/request-catalog.yml` | `tools/schemas/request-catalog.schema.json` |
| Параметры изменений | `ops/change-catalog.yml` | `tools/schemas/change-catalog.schema.json` |
| Требования | `requirements.yml` | `tools/schemas/service-requirements.schema.json` |

---

## Инструменты CI

```bash
# Валидировать все machine-readable файлы сервисов
make validate-services

# Линт Markdown-файлов
make lint-docs
```

---

## Примеры

| Услуга | Продукт | Профиль |
|---|---|---|
| [`vtsod-vmwr-vs/`](./vtsod-vmwr-vs/) | `products/private-cloud/` | Extended |
