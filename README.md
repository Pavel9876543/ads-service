# 🚀 FastAPI Advertisement Service

REST API сервис объявлений купли/продажи с системой пользователей, JWT-авторизацией и разграничением прав доступа, реализованный на **FastAPI** с поддержкой **Docker**.

---

## ✨ Возможности

### 📢 Объявления

* ➕ Создание объявления
* 🔍 Получение объявления по ID
* ✏️ Обновление объявления
* ❌ Удаление объявления
* 🔎 Поиск объявлений по параметрам:

  * `title`
  * `description`
  * `author`
  * `min_price`
  * `max_price`
  * `created_after`
  * `created_before`

---

### 👤 Пользователи

* ➕ Регистрация пользователя
* 🔍 Получение пользователя по ID
* ✏️ Обновление пользователя
* ❌ Удаление пользователя

---

### 🔐 Авторизация

* JWT authentication
* Срок действия токена — 48 часов
* Хранение паролей в хешированном виде
* Разграничение прав доступа:
  * `user`
  * `admin`

---

# 🛠 Технологии

* FastAPI
* SQLAlchemy
* SQLite
* JWT (python-jose)
* Passlib (bcrypt)
* Docker
* Uvicorn

---

# 📁 Структура проекта

```text
.
├── app
│   ├── auth.py
│   ├── security.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── database.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

# ⚙️ Запуск проекта

## 1. Клонирование репозитория

```bash
git clone https://github.com/Pavel9876543/ads-service.git
cd ads-service
```

---

## 2. Запуск через Docker

```bash
docker compose up --build
```

---

# 🌐 Доступные адреса

| Сервис     | URL                           |
| ---------- | ----------------------------- |
| API        | `http://localhost:8000`       |
| Swagger UI | `http://localhost:8000/docs`  |
| ReDoc      | `http://localhost:8000/redoc` |

---

# 🔐 Авторизация

## Логин

### `POST /login`

### Request

```json
{
  "username": "ivan",
  "password": "1234"
}
```

### Response

```json
{
  "token": "jwt_token"
}
```

---

## Использование токена

Передавайте JWT токен в заголовке:

```http
Authorization: Bearer <token>
```

---

# 👥 Роли и права доступа

## 🔓 Неавторизованный пользователь

Доступно:

* POST `/user`
* GET `/user/{user_id}`
* GET `/advertisement/{id}`
* GET `/advertisement`

---

## 👤 Пользователь с ролью `user`

Доступно:

* все права неавторизованного пользователя
* PATCH `/user/{user_id}` — только свои данные
* DELETE `/user/{user_id}` — только себя
* POST `/advertisement`
* PATCH `/advertisement/{id}` — только свои объявления
* DELETE `/advertisement/{id}` — только свои объявления

---

## 👑 Пользователь с ролью `admin`

Доступны любые действия с любыми сущностями.

---

# 📌 API Endpoints

## 📢 Advertisement API

| Метод  | Endpoint              | Описание              |
| ------ | --------------------- | --------------------- |
| POST   | `/advertisement`      | Создание объявления   |
| GET    | `/advertisement/{id}` | Получение объявления  |
| PATCH  | `/advertisement/{id}` | Обновление объявления |
| DELETE | `/advertisement/{id}` | Удаление объявления   |
| GET    | `/advertisement`      | Поиск объявлений      |

---

## 👤 User API

| Метод  | Endpoint          | Описание                |
| ------ | ----------------- | ----------------------- |
| POST   | `/user`           | Создание пользователя   |
| GET    | `/user/{user_id}` | Получение пользователя  |
| PATCH  | `/user/{user_id}` | Обновление пользователя |
| DELETE | `/user/{user_id}` | Удаление пользователя   |

---

## 🔐 Auth API

| Метод | Endpoint | Описание |
| ------ | -------- | -------- |
| POST | `/login` | Получение JWT токена |

---

# ➕ Создание пользователя

## Request

### `POST /user`

```json
{
  "username": "ivan",
  "password": "1234"
}
```

---

# 🔐 Авторизация пользователя

## Request

### `POST /login`

```json
{
  "username": "ivan",
  "password": "1234"
}
```

---

## Response

```json
{
  "token": "jwt_token"
}
```

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
  "created_at": "2026-05-20T12:00:00",
  "owner_id": 1
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

---

# 🔎 Поиск объявлений

### `GET /advertisement`

## Примеры запросов

Поиск по названию:

```http
/advertisement?title=iPhone
```

---

Поиск по описанию:

```http
/advertisement?description=отличное
```

---

Поиск по автору:

```http
/advertisement?author=Николай
```

---

Поиск по диапазону цены:

```http
/advertisement?min_price=10000&max_price=70000
```

---

Поиск по дате создания:

```http
/advertisement?created_after=2025-01-01T00:00:00
```

---

Комбинированный поиск:

```http
/advertisement?title=iPhone&author=Николай
```

---

# 🧪 Примеры curl запросов

## Создание пользователя

```bash
curl -X POST http://localhost:8000/user \
-H "Content-Type: application/json" \
-d '{
  "username": "ivan",
  "password": "1234"
}'
```

---

## Авторизация

```bash
curl -X POST http://localhost:8000/login \
-H "Content-Type: application/json" \
-d '{
  "username": "ivan",
  "password": "1234"
}'
```

---

## Создание объявления

```bash
curl -X POST http://localhost:8000/advertisement \
-H "Authorization: Bearer <token>" \
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
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{
  "price": 60000
}'
```

---

## Удаление объявления

```bash
curl -X DELETE http://localhost:8000/advertisement/1 \
-H "Authorization: Bearer <token>"
```

---

# 📌 HTTP Status Codes

| Code | Description |
| ---- | ----------- |
| 200 | Success |
| 201 | Created |
| 204 | Deleted successfully |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |

---

# 👨‍💻 Автор

Гусев Павел