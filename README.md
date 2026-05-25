# 🚀 FastAPI Advertisement Service

REST API сервис объявлений купли/продажи, реализованный на **FastAPI** с поддержкой **Docker**.

---

## ✨ Возможности

* ➕ Создание объявления
* 🔍 Получение объявления по ID
* ✏️ Обновление объявления
* ❌ Удаление объявления
* 🔎 Поиск объявлений по параметрам:

  * `title`
  * `author`
  * `min_price`
  * `max_price`

---

# 🛠 Технологии

* FastAPI
* SQLAlchemy
* SQLite
* Docker
* Uvicorn

---

# 📁 Структура проекта

```text
.
├── app
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── database.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

# ⚙️ Запуск проекта

## 1. Клонирование репозитория

```bash
git clone <repository_url>
cd fastapi-ads-service
```

---

## 2. Запуск через Docker

```bash
docker-compose up --build
```

---

# 🌐 Доступные адреса

| Сервис     | URL                           |
| ---------- | ----------------------------- |
| API        | `http://localhost:8000`       |
| Swagger UI | `http://localhost:8000/docs`  |
| ReDoc      | `http://localhost:8000/redoc` |

---

# 📌 API Endpoints

| Метод  | Endpoint              | Описание              |
| ------ | --------------------- | --------------------- |
| POST   | `/advertisement`      | Создание объявления   |
| GET    | `/advertisement/{id}` | Получение объявления  |
| PATCH  | `/advertisement/{id}` | Обновление объявления |
| DELETE | `/advertisement/{id}` | Удаление объявления   |
| GET    | `/advertisement`      | Поиск объявлений      |

---

# ➕ Создание объявления

## Request

### `POST /advertisement`

```json
{
  "title": "iPhone 13",
  "description": "128GB, отличное состояние",
  "price": 65000,
  "author": "Николай"
}
```

---

## Response

```json
{
  "id": 1,
  "title": "iPhone 13",
  "description": "128GB, отличное состояние",
  "price": 65000,
  "author": "Николай",
  "created_at": "2026-05-20T12:00:00"
}
```

---

# 🔍 Получение объявления

### `GET /advertisement/{id}`

Пример:

```http
GET /advertisement/1
```

---

# ✏️ Обновление объявления

### `PATCH /advertisement/{id}`

Request body:

```json
{
  "price": 60000
}
```

---

# ❌ Удаление объявления

### `DELETE /advertisement/{id}`

Response:

```json
{
  "status": "deleted"
}
```

---

# 🔎 Поиск объявлений

### `GET /advertisement`

## Примеры запросов

Поиск по названию:

```http
/advertisement?title=iPhone
```

Поиск по автору:

```http
/advertisement?author=Николай
```

Поиск по диапазону цены:

```http
/advertisement?min_price=10000&max_price=70000
```

Комбинированный поиск:

```http
/advertisement?title=iPhone&author=Николай
```

---

# 🧪 Примеры curl запросов

## Создание объявления

```bash
curl -X POST http://localhost:8000/advertisement \
-H "Content-Type: application/json" \
-d '{
  "title": "iPhone 13",
  "description": "128GB, отличное состояние",
  "price": 65000,
  "author": "Николай"
}'
```

---

## Получение объявления

```bash
curl http://localhost:8000/advertisement/1
```

---

## Обновление объявления

```bash
curl -X PATCH http://localhost:8000/advertisement/1 \
-H "Content-Type: application/json" \
-d '{
  "price": 60000
}'
```

---

## Удаление объявления

```bash
curl -X DELETE http://localhost:8000/advertisement/1
```

---

# 👨‍💻 Автор

Гусев Павел
