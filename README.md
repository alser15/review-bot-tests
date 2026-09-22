# Random String Service

Микросервис на FastAPI с одной ручкой: принимает длину в виде числа и возвращает случайную строку этой длины.

## Стек

- Python 3.10+
- FastAPI
- uvicorn

## Локальный запуск

### 1. Создать и активировать виртуальное окружение

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Запустить сервис

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Swagger

После запуска Swagger UI доступен по адресу:

- http://localhost:8000/docs

В Swagger можно вызвать ручку `/random-string` — нажмите «Try it out», введите длину и выполните запрос.

## Ручка

### `GET /random-string`

Синхронная ручка. Принимает длину в виде числа (query-параметр `length`) и возвращает случайную строку этой длины.

**Параметры:**

- `length` (int, обязательный) — длина генерируемой строки, должна быть больше нуля.

**Пример запроса:**

```bash
curl "http://localhost:8000/random-string?length=10"
```

**Пример ответа:**

```json
{
  "length": 10,
  "result": "aB3xK9mQ2z"
}
```

**Ошибки:**

- `400` — если длина равна нулю.
- `422` — если параметр `length` не является неотрицательным числом.
