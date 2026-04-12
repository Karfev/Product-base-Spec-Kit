# AI Quality Gates — Five Pillars (SpecKit Edition)

> Кодифицированные ограничения качества для implementation phase.
> Применяется: Standard+ профиль, фазы T2a/T2b в tasks.md.
> REQ-QUAL-004.

---

## Когда применять

- **Standard, Extended, Enterprise** профили — обязательно
- **Minimal** — не применяется (quick fix, overhead не оправдан)
- **Фаза:** T2a (написание тестов) и T2b (реализация) в `/speckit-implement`

---

## Pillar 1: Decomposition (Декомпозиция)

**Правила:**
- Max **50 LOC** per method/function (excluding comments and blank lines)
- Max **7-9 объектов/сущностей** в активном scope per task
- **Single Responsibility:** одна функция = одна задача
- Если метод > 50 LOC → декомпозировать до продолжения

**Пример (хорошо):**
```python
def validate_request(req):
    """Validate incoming request. 12 LOC."""
    check_auth(req.headers)
    check_schema(req.body)
    check_rate_limit(req.client_id)

def check_auth(headers):
    """Verify auth token. 8 LOC."""
    ...
```

**Anti-pattern:**
```python
def handle_request(req):
    """Everything in one method. 200+ LOC."""
    # auth check...
    # schema validation...
    # rate limit...
    # business logic...
    # response formatting...
    # error handling...
```

**Enforcement:** `/speckit-implement` проверяет: "Метод {name} = {N} строк. Decompose?"

---

## Pillar 2: Test-First (TDD)

**Правила:**
- **T2a MUST complete before T2b** starts
- Тесты определяют интерфейс: write test → derive function signature → implement
- **Arrange-Act-Assert** pattern для unit tests
- Contract tests валидируют OpenAPI/AsyncAPI compliance

**Пример (хорошо):**
```python
# T2a: Write failing test FIRST
def test_create_api_key_returns_201():
    response = client.post("/api-keys", json={"name": "test"})
    assert response.status_code == 201
    assert "id" in response.json()

# T2b: THEN implement to make it pass
@app.post("/api-keys")
def create_api_key(req: CreateKeyRequest):
    key = service.create(req.name)
    return {"id": key.id}, 201
```

**Anti-pattern:**
- Написать реализацию, потом подогнать тесты
- Тесты без assertions (test that passes by default)
- T2b без T2a → CI warning

**Enforcement:**
- `/speckit-implement` блокирует T2b если T2a не marked done
- `check-spec-quality.py`: T2b `[x]` before T2a `[x]` → CI warning

---

## Pillar 3: Architecture-First (Архитектура в первую очередь)

**Правила:**
- Создать **skeleton stubs** (interfaces, type signatures, empty handlers) до реализации
- Stubs **MUST match contract signatures** (OpenAPI paths, AsyncAPI handlers)
- Реализовать **один метод за раз**, не целый модуль

**Пример (хорошо):**
```python
# Step 1: Stub matching OpenAPI contract
@app.post("/api-keys")
def create_api_key(req: CreateKeyRequest) -> CreateKeyResponse:
    raise NotImplementedError  # stub

@app.delete("/api-keys/{key_id}")
def delete_api_key(key_id: str) -> None:
    raise NotImplementedError  # stub

# Step 2: Implement one at a time
@app.post("/api-keys")
def create_api_key(req: CreateKeyRequest) -> CreateKeyResponse:
    key = service.create(req.name)
    return CreateKeyResponse(id=key.id, created_at=key.created_at)
```

**Anti-pattern:**
- Реализовать всю бизнес-логику без skeleton stubs
- Stubs с другими signatures чем в OpenAPI

**Enforcement:** `/speckit-implement` спрашивает: "Stubs created and match contracts? [Y/N]"

---

## Pillar 4: Focused Work (Фокусированная работа)

**Правила:**
- **One task = one bounded context** (single handler, single endpoint, single event)
- Explicit scope boundaries перед каждым T2b: "This task covers: {files}, {methods}"
- **No side-effect changes** outside declared scope

**Пример (хорошо):**
```
Scope for T2b: 
- File: src/handlers/api_keys.py
- Methods: create_api_key()
- Contract: POST /api-keys (openapi.yaml)
```

**Anti-pattern:**
- "While I'm here, let me also refactor the auth module"
- Touching 10 files in one task
- No declared scope → changes leak everywhere

**Enforcement:** `/speckit-implement` prompts: "Scope for this task: {declared scope}. Proceed? [Y/N]"

---

## Pillar 5: Contract-Aware (Контрактная осведомлённость)

> Специфика SpecKit — differentiator vs generic AI quality frameworks.

**Правила:**
- Implementation **MUST match contract signatures:**
  - REST: HTTP method + path + request/response schemas from OpenAPI
  - Events: channel + message schema from AsyncAPI
  - Data: entity schemas from `contracts/schemas/*.json`
- **`make lint-contracts` MUST pass** before T2b
- Breaking changes: require ADR + deprecation plan

**Пример (хорошо):**
```yaml
# openapi.yaml defines:
paths:
  /api-keys:
    post:
      requestBody:
        schema: { $ref: '#/components/schemas/CreateKeyRequest' }
      responses:
        201:
          schema: { $ref: '#/components/schemas/CreateKeyResponse' }
```
```python
# Implementation matches contract exactly:
@app.post("/api-keys", status_code=201)
def create_api_key(req: CreateKeyRequest) -> CreateKeyResponse:
    ...
```

**Anti-pattern:**
- Endpoint returns 200 instead of 201 (contract says 201)
- Request body has different field names than schema
- Missing contract for new endpoint

**Enforcement:**
- `/speckit-implement` runs `make lint-contracts` before T2b
- Mismatch → blocker with specific diff

---

## Pre-flight Checklist (для /speckit-implement)

Before starting T2b, verify:

- [ ] T2a tests written and failing (RED)?
- [ ] Architecture stubs created?
- [ ] Stubs match contracts (`make lint-contracts`)?
- [ ] Scope declared (which files, which methods)?
- [ ] Quality gates document read?

If any item unchecked → WARNING with specific blocker.
If all checked → proceed to implementation.
