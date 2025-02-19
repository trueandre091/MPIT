from fastapi import status

# Описания эндпоинтов
get_sessions_description = """
Получить список всех активных сессий текущего пользователя.

Возвращает:
- Общее количество активных сессий
- Список сессий с информацией о каждой:
  - ID сессии
  - User-Agent браузера
  - IP-адрес
  - Информация об устройстве
  - Статус активности
  - Дата создания
  - Дата последней активности
"""

terminate_session_description = """
Завершить указанную сессию пользователя.

Пользователь может завершить только свои собственные сессии.
После завершения сессия становится неактивной и связанные с ней токены становятся недействительными.
"""

terminate_all_sessions_description = """
Завершить все активные сессии текущего пользователя, кроме текущей.

Полезно при подозрении на компрометацию учетной записи или для выхода со всех других устройств.
Текущая сессия остается активной, чтобы пользователь не был разлогинен.
"""

refresh_session_description = """
Обновить текущую сессию, используя refresh token.

Требуется передать refresh token в заголовке запроса X-Refresh-Token.

Процесс обновления:
- Проверяет валидность refresh token
- Создает новую пару access/refresh токенов
- Деактивирует старую сессию
- Создает новую сессию с обновленными токенами
- Сохраняет информацию об устройстве
"""

# Описания ответов
get_sessions_responses = {
    status.HTTP_200_OK: {
        "description": "Успешное получение списка сессий",
        "content": {
            "application/json": {
                "example": {
                    "total": 2,
                    "sessions": [
                        {
                            "id": 1,
                            "user_agent": "Mozilla/5.0...",
                            "ip_address": "192.168.1.1",
                            "device_info": {
                                "browser": {"family": "Chrome", "version": "120.0.0"},
                                "os": {"family": "Windows", "version": "10"},
                                "device": {"family": "Other", "brand": None, "model": None},
                                "is_mobile": False,
                                "is_pc": True
                            },
                            "is_active": True,
                            "created_at": "2024-02-19T12:00:00",
                            "last_activity": "2024-02-19T12:30:00"
                        }
                    ]
                }
            }
        }
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Ошибка аутентификации",
        "content": {
            "application/json": {
                "example": {"detail": "Не удалось проверить учетные данные"}
            }
        }
    }
}

terminate_session_responses = {
    status.HTTP_200_OK: {
        "description": "Сессия успешно завершена",
        "content": {
            "application/json": {
                "example": {
                    "message": "Сессия успешно завершена",
                    "session": {
                        "id": 1,
                        "user_agent": "Mozilla/5.0...",
                        "ip_address": "192.168.1.1",
                        "device_info": {
                            "browser": {"family": "Chrome", "version": "120.0.0"},
                            "os": {"family": "Windows", "version": "10"},
                            "device": {"family": "Other", "brand": None, "model": None},
                            "is_mobile": False,
                            "is_pc": True
                        },
                        "is_active": False,
                        "created_at": "2024-02-19T12:00:00",
                        "last_activity": "2024-02-19T12:30:00"
                    }
                }
            }
        }
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Сессия не найдена",
        "content": {
            "application/json": {
                "example": {"detail": "Сессия не найдена или не принадлежит текущему пользователю"}
            }
        }
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Ошибка аутентификации",
        "content": {
            "application/json": {
                "example": {"detail": "Не удалось проверить учетные данные"}
            }
        }
    }
}

terminate_all_sessions_responses = {
    status.HTTP_200_OK: {
        "description": "Все сессии успешно завершены",
        "content": {
            "application/json": {
                "example": {
                    "message": "Все остальные сессии успешно завершены"
                }
            }
        }
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Ошибка аутентификации",
        "content": {
            "application/json": {
                "example": {"detail": "Не удалось проверить учетные данные"}
            }
        }
    }
}

refresh_session_responses = {
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
                        "is_active": True,
                        "role": "user"
                    }
                }
            }
        }
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Ошибка обновления токенов",
        "content": {
            "application/json": {
                "examples": {
                    "no_token": {
                        "summary": "Refresh token не предоставлен",
                        "value": {"detail": "Refresh token не предоставлен"}
                    },
                    "invalid_token": {
                        "summary": "Недействительный refresh token",
                        "value": {"detail": "Недействительный refresh token"}
                    },
                    "user_not_found": {
                        "summary": "Пользователь не найден",
                        "value": {"detail": "Пользователь не найден"}
                    }
                }
            }
        }
    }
} 