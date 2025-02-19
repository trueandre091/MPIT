register_responses = {
    201: {
        "description": "Успешная регистрация",
        "content": {
            "application/json": {
                "example": {
                    "access_token": "eyJhbGciOiJIUzI1NiIs...",
                    "token_type": "bearer"
                }
            }
        }
    },
    400: {
        "description": "Ошибка валидации",
        "content": {
            "application/json": {
                "examples": {
                    "email": {
                        "value": {"detail": "Email already registered"}
                    },
                    "password": {
                        "value": {"detail": "Password must contain at least 8 characters..."}
                    },
                    "full_name": {
                        "value": {"detail": "Full name must contain only letters"}
                    }
                }
            }
        }
    }
}

login_responses = {
    200: {
        "description": "Успешная авторизация",
        "content": {
            "application/json": {
                "example": {
                    "access_token": "eyJhbGciOiJIUzI1NiIs...",
                    "token_type": "bearer"
                }
            }
        }
    },
    401: {
        "description": "Ошибка авторизации",
        "content": {
            "application/json": {
                "example": {"detail": "Incorrect email or password"}
            }
        }
    },
    422: {
        "description": "Ошибка валидации",
        "content": {
            "application/json": {
                "example": {"detail": "Invalid email format"}
            }
        }
    }
}

register_description = """
Регистрация нового пользователя.

- **email**: Email пользователя (должен быть уникальным)
- **password**: Пароль (минимум 8 символов, одна заглавная буква, одна строчная буква, одна цифра, один специальный символ)
- **full_name**: Полное имя пользователя (только буквы и пробелы, от 2 до 50 символов)

Returns:
    Token: JWT токен для авторизации
"""

login_description = """
Авторизация пользователя.

- **username**: Email пользователя (используется как username)
- **password**: Пароль

Returns:
    Token: JWT токен для авторизации

Примечание:
    Используйте полученный токен в формате "Bearer {token}" для авторизации
"""

refresh_description = """
Обновление токена.

Требует действующего токена для получения нового.

Returns:
    Token: Новый JWT токен
""" 