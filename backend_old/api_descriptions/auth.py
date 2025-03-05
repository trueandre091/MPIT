from fastapi import status

register_description = """
Регистрация нового пользователя.

Требования к данным:
- Email: должен быть валидным email адресом
- Пароль: 
  * Минимум 8 символов
  * Максимум 64 символа
  * Хотя бы одна заглавная буква (A-Z)
  * Хотя бы одна строчная буква (a-z)
  * Хотя бы одна цифра (0-9)
  * Хотя бы один специальный символ (!@#$%^&*(),.?":{}|<>)
- Полное имя:
  * От 2 до 50 символов
  * Только буквы и пробелы

При успешной регистрации возвращает:
- access_token: для авторизации запросов
- refresh_token: для обновления access_token
- token_type: тип токена (bearer)
- user: информация о пользователе

Возможные ошибки:
- 409: Email уже зарегистрирован
- 422: Ошибки валидации данных (возвращает список ошибок по каждому полю)
"""

login_description = """
Вход в систему.

Требования к данным:
- Email: должен быть валидным email адресом
- Пароль: должен соответствовать требованиям безопасности

При успешном входе возвращает:
- access_token: для авторизации запросов
- refresh_token: для обновления access_token
- token_type: тип токена (bearer)
- user: информация о пользователе

Возможные ошибки:
- 401: Неверный email или пароль
- 403: Аккаунт заблокирован
- 422: Ошибки валидации данных (возвращает список ошибок по каждому полю)
"""

refresh_description = """
Обновление токенов с помощью refresh token.

Требуется передать:
1. refresh token в заголовке X-Refresh-Token
2. Формат: X-Refresh-Token: <refresh_token> (без Bearer)

Возможные ошибки:
- 401: Отсутствует или недействительный refresh token
- 403: Сессия не найдена или истекла
- 404: Пользователь не найден

При успешном обновлении:
- Обновляются токены в существующей сессии
- Возвращаются новые access и refresh токены

Для последующих запросов используйте новый access token в заголовке:
Authorization: Bearer <access_token>
"""

register_responses = {
    status.HTTP_201_CREATED: {
        "description": "Пользователь успешно зарегистрирован",
        "content": {
            "application/json": {
                "example": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "full_name": "Иван Иванов",
                        "role": "user"
                    }
                }
            }
        }
    },
    status.HTTP_400_BAD_REQUEST: {
        "description": "Ошибка валидации данных",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Этот email уже зарегистрирован"
                }
            }
        }
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "Ошибка валидации данных",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_email": {
                        "summary": "Неверный формат email",
                        "value": {
                            "detail": [
                                {
                                    "type": "value_error",
                                    "loc": ["email"],
                                    "msg": "Неверный формат email",
                                    "input": "invalid-email"
                                }
                            ]
                        }
                    },
                    "invalid_password": {
                        "summary": "Неверный формат пароля",
                        "value": {
                            "detail": "Пароль должен содержать:\n- Минимум 8 символов\n- Хотя бы одну заглавную букву (A-Z)\n- Хотя бы одну строчную букву (a-z)\n- Хотя бы одну цифру (0-9)\n- Хотя бы один специальный символ (@$!%*?&#)"
                        }
                    },
                    "invalid_name": {
                        "summary": "Неверный формат имени",
                        "value": {
                            "detail": "Имя должно содержать:\n- Только буквы (русские или английские) и пробелы\n- Длину от 2 до 50 символов"
                        }
                    }
                }
            }
        }
    }
}

login_responses = {
    status.HTTP_200_OK: {
        "description": "Успешная авторизация",
        "content": {
            "application/json": {
                "example": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "full_name": "Иван Иванов",
                        "role": "user"
                    }
                }
            }
        }
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Ошибка авторизации",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Incorrect email or password"
                }
            }
        }
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "Ошибка валидации данных",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid email format"
                }
            }
        }
    }
}

refresh_responses = {
    status.HTTP_200_OK: {
        "description": "Токены успешно обновлены",
        "content": {
            "application/json": {
                "example": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "full_name": "Иван Иванов",
                        "role": "user"
                    }
                }
            }
        }
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Ошибка аутентификации",
        "content": {
            "application/json": {
                "examples": {
                    "no_token": {
                        "summary": "Заголовок X-Refresh-Token отсутствует",
                        "value": {
                            "detail": "Refresh token не предоставлен"
                        }
                    },
                    "invalid_token": {
                        "summary": "Недействительный refresh token",
                        "value": {
                            "detail": "Недействительный refresh token"
                        }
                    }
                }
            }
        }
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "Сессия истекла или недействительна",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Сессия не найдена или истекла"
                }
            }
        }
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Пользователь не найден",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Пользователь не найден"
                }
            }
        }
    }
} 