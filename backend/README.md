# FastAPI Backend

backend-приложение на FastAPI с реализованной системой аутентификации, сессиями и ролями пользователей.

## Основные возможности

- 🔐 **Аутентификация и авторизация**:
  - Регистрация и вход через email/пароль
  - JWT токены (access + refresh)
  - Управление сессиями пользователей
  - Система ролей (admin/user)

- 📝 **Готовые эндпоинты**:
  - Регистрация (`/auth/register`)
  - Вход (`/auth/login`)
  - Выход (`/auth/logout`)
  - Обновление токенов (`/auth/refresh`)
  - Информация о пользователе (`/auth/me`)
  - Управление сессиями (`/sessions/*`)

- 🛠 **Технический стек**:
  - FastAPI
  - SQLAlchemy
  - Alembic
  - PostgreSQL
  - JWT
  - Pydantic v2

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных

1. Создайте базу данных PostgreSQL (либо введите в терминале команду ниже **, но только после настройки .env (п. 3)!**)

```bash
python scripts\create_database.py
```

2. Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```
3. Отредактируйте `.env` файл:
```env
# База данных
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Безопасность
SECRET_KEY=your-secret-key-here  # Сгенерируйте свой ключ
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Настройки приложения
APP_NAME=FastAPI Backend
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=True
API_PREFIX=/api/v1

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 5. Применение миграций

```bash
alembic upgrade head
```

### 6. Запуск приложения

```bash
uvicorn main:app --reload
```

Приложение будет доступно по адресу: `http://localhost:8000`

Swagger UI: `http://localhost:8000/docs`
Redoc: `http://localhost:8000/redoc`

## Структура проекта

```
├── alembic/              # Миграции базы данных
├── api_descriptions/     # Описания API для Swagger
├── models/              # Модели SQLAlchemy
├── routers/            # Маршруты FastAPI
├── schemas/            # Pydantic модели
├── services/           # Бизнес-логика
├── .env               # Конфигурация
├── main.py            # Точка входа
└── requirements.txt   # Зависимости
```

## Создание первого администратора

После запуска приложения зарегистрируйте пользователя через `/auth/register`, затем обновите его роль в базе данных:

```sql
UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';
```

## API Endpoints

### Аутентификация

- `POST /api/v1/auth/register` - Регистрация нового пользователя
- `POST /api/v1/auth/login` - Вход в систему
- `POST /api/v1/auth/logout` - Выход из системы
- `POST /api/v1/auth/refresh` - Обновление токенов
- `GET /api/v1/auth/me` - Информация о текущем пользователе

### Сессии

- `GET /api/v1/sessions/me` - Список активных сессий
- `DELETE /api/v1/sessions/{session_id}` - Удаление конкретной сессии
- `DELETE /api/v1/sessions/me/all` - Удаление всех сессий пользователя

### Пользователи (только для админов)

- `GET /api/v1/users` - Список всех пользователей
- `GET /api/v1/users/{user_id}` - Информация о пользователе
- `PATCH /api/v1/users/{user_id}` - Обновление пользователя
- `DELETE /api/v1/users/{user_id}` - Удаление пользователя

## Безопасность

- Все пароли хешируются с использованием bcrypt
- Используется система JWT с access и refresh токенами
- Access token действителен 30 минут
- Refresh token действителен 7 дней

## Дополнительные возможности

1. **Автоматическая очистка сессий**:
   ```python
   from models.session import Session
   
   # Очистка всех истекших сессий
   Session.cleanup_expired_sessions(db)
   ```

2. **Получение информации об устройстве**:
   ```python
   from routers.auth import parse_user_agent
   
   device_info = parse_user_agent(user_agent_string)
   ```

## Разработка

1. **Создание новой миграции**:
   ```bash
   alembic revision --autogenerate -m "description"
   ```

2. **Применение миграций**:
   ```bash
   alembic upgrade head
   ```

3. **Откат миграции**:
   ```bash
   alembic downgrade -1
   ```
