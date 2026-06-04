# 🚀 FastAPI Advertisement Service

REST API сервис объявлений купли/продажи с JWT-аутентификацией, ролевой моделью доступа и PostgreSQL.

## Технологии

* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT (python-jose)
* Passlib (bcrypt)
* Docker
* Docker Compose

---

## Запуск

```bash
git clone https://github.com/Pavel9876543/ads-service.git
cd ads-service

docker compose up --build
```

API будет доступен:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

## Роли

### Неавторизованный пользователь

Доступно:

* POST /user
* GET /user/{user_id}
* GET /advertisement/{id}
* GET /advertisement

### User

Дополнительно:

* PATCH /user/{user_id} (только себя)
* DELETE /user/{user_id} (только себя)
* POST /advertisement
* PATCH /advertisement/{id} (только свои объявления)
* DELETE /advertisement/{id} (только свои объявления)

### Admin

Полный доступ ко всем пользователям и объявлениям.

---

## API

### Auth

| Метод | Endpoint |
| ----- | -------- |
| POST  | /login   |

### Users

| Метод  | Endpoint        |
| ------ | --------------- |
| POST   | /user           |
| GET    | /user           |
| GET    | /user/{user_id} |
| PATCH  | /user/{user_id} |
| DELETE | /user/{user_id} |

### Advertisements

| Метод  | Endpoint            |
| ------ | ------------------- |
| POST   | /advertisement      |
| GET    | /advertisement      |
| GET    | /advertisement/{id} |
| PATCH  | /advertisement/{id} |
| DELETE | /advertisement/{id} |

---

## Создание пользователя

```json
{
  "username": "admin",
  "password": "1234",
  "role": "admin"
}
```

Допустимые роли:

```text
user
admin
```

---

## Авторизация

Запрос:

```json
{
  "username": "admin",
  "password": "1234"
}
```

Ответ:

```json
{
  "token": "jwt_token"
}
```

Использование токена:

```http
Authorization: Bearer <token>
```

---

## Создание объявления

```json
{
  "title": "iPhone 13",
  "description": "128GB, отличное состояние",
  "price": 65000,
  "author": "Павел"
}
```

---

## Поиск объявлений

Поддерживаемые параметры:

```text
title
description
author
min_price
max_price
created_after
created_before
limit
offset
```

Примеры:

```http
GET /advertisement?title=iPhone
```

```http
GET /advertisement?author=Павел
```

```http
GET /advertisement?min_price=10000&max_price=70000
```

```http
GET /advertisement?created_after=2025-01-01T00:00:00
```

```http
GET /advertisement?limit=10&offset=20
```

```http
GET /advertisement?title=iPhone&author=Павел&limit=10
```

---

## Быстрая проверка через curl

Создать пользователя:

```bash
curl -X POST http://localhost:8000/user \
-H "Content-Type: application/json" \
-d '{
  "username":"admin",
  "password":"1234",
  "role":"admin"
}'
```

Получить токен:

```bash
curl -X POST http://localhost:8000/login \
-H "Content-Type: application/json" \
-d '{
  "username":"admin",
  "password":"1234"
}'
```

Создать объявление:

```bash
curl -X POST http://localhost:8000/advertisement \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{
  "title":"iPhone 13",
  "description":"128GB",
  "price":65000,
  "author":"Павел"
}'
```

---

## Структура проекта

```text
.
├── app
│   ├── auth.py
│   ├── security.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Автор

Павел Гусев