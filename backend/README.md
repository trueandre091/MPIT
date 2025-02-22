# FastAPI Backend Template для хакатонов

Готовый шаблон backend-приложения на FastAPI с реализованной системой аутентификации, сессиями и ролями пользователей.

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

1. Создайте базу данных PostgreSQL (либо введите в терминале команду ниже после пункта 3)

```bash
python scripts\create_database.py
```

2. Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```
3. Отредактируйте `.env` файл:
```env
# Настройки окружения
ENVIRONMENT=development  # development или production

# Настройки приложения
APP_NAME=FastAPI Template
APP_VERSION=1.0.0

# Настройки сервера
HOST=localhost  # development: localhost, production: 0.0.0.0
PORT=8000

# Настройки базы данных
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password-here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fastapi_db

# JWT settings
SECRET_KEY=your-secret-key-here  # Изменить в production!
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1  # development: 30, production: 60

# CORS settings (разделять запятыми)
DEV_CORS_ORIGINS=http://localhost:3000,http://localhost:8080
PROD_CORS_ORIGINS=https://your-production-domain.com
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

Swagger UI: `http://localhost:8000/api/v1/docs`
Redoc: `http://localhost:8000/api/v1/redoc`

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

## Генерация секретного ключа

Для генерации безопасного секретного ключа используйте Python:

```python
import secrets
print(secrets.token_hex(32))
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
- Каждая сессия привязана к устройству пользователя
- Поддерживается одновременная работа с нескольких устройств
- Возможность завершения всех сессий кроме текущей

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

## Лицензия

MIT 