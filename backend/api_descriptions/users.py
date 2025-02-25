from fastapi import status

get_current_user_responses = {
    status.HTTP_200_OK: {
        "description": "Успешное получение информации о пользователе",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "email": "user@example.com",
                    "full_name": "Иван Иванов",
                    "is_active": True,
                    "role": "user",
                    "created_at": "2024-02-19T12:00:00",
                    "updated_at": "2024-02-19T12:00:00"
                }
            }
        }
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Ошибка аутентификации",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_token": {
                        "summary": "Недействительный токен",
                        "value": {"detail": "Не удалось проверить учетные данные"}
                    },
                    "expired_token": {
                        "summary": "Истекший токен",
                        "value": {"detail": "Срок действия токена истек"}
                    }
                }
            }
        }
    }
}

update_user_responses = {
    status.HTTP_200_OK: {
        "description": "Информация о пользователе успешно обновлена",
        "content": {
            "application/json": {
                "examples": {
                    "user_update": {
                        "summary": "Обновление обычным пользователем",
                        "value": {
                            "id": 1,
                            "email": "new.email@example.com",
                            "full_name": "Новое Имя",
                            "is_active": True,
                            "role": "user",
                            "created_at": "2024-02-19T12:00:00",
                            "updated_at": "2024-02-19T12:30:00"
                        }
                    },
                    "admin_update": {
                        "summary": "Обновление администратором",
                        "value": {
                            "id": 1,
                            "email": "new.email@example.com",
                            "full_name": "Новое Имя",
                            "is_active": False,
                            "role": "admin",
                            "created_at": "2024-02-19T12:00:00",
                            "updated_at": "2024-02-19T12:30:00"
                        }
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
                    "missing_token": {
                        "summary": "Отсутствует токен",
                        "value": {
                            "detail": "Отсутствует токен авторизации"
                        }
                    },
                    "invalid_token": {
                        "summary": "Недействительный токен",
                        "value": {
                            "detail": "Не удалось проверить учетные данные"
                        }
                    },
                    "expired_token": {
                        "summary": "Истекший токен",
                        "value": {
                            "detail": "Срок действия токена истек"
                        }
                    }
                }
            }
        }
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "Доступ запрещен",
        "content": {
            "application/json": {
                "examples": {
                    "role_change": {
                        "summary": "Попытка изменить роль",
                        "value": {
                            "detail": "Поле 'role' может изменять только администратор"
                        }
                    },
                    "status_change": {
                        "summary": "Попытка изменить статус",
                        "value": {
                            "detail": "Поле 'is_active' может изменять только администратор"
                        }
                    }
                }
            }
        }
    },
    status.HTTP_409_CONFLICT: {
        "description": "Конфликт данных",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Этот email уже используется"
                }
            }
        }
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "Ошибка валидации",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_email": {
                        "summary": "Неверный формат email",
                        "value": {
                            "detail": "Введите корректный email адрес"
                        }
                    },
                    "invalid_password": {
                        "summary": "Неверный формат пароля",
                        "value": {
                            "detail": "Пароль должен содержать минимум 8 символов, заглавные и строчные буквы, цифры и спецсимволы"
                        }
                    },
                    "invalid_name": {
                        "summary": "Неверный формат имени",
                        "value": {
                            "detail": "Имя должно содержать от 2 до 50 символов"
                        }
                    }
                }
            }
        }
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Внутренняя ошибка сервера",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Ошибка при обновлении пользователя"
                }
            }
        }
    }
}

delete_user_responses = {
    status.HTTP_200_OK: {
        "description": "Пользователь успешно удален",
        "content": {
            "application/json": {
                "example": {
                    "message": "Пользователь успешно удален"
                }
            }
        }
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Ошибка аутентификации",
        "content": {
            "application/json": {
                "examples": {
                    "invalid_token": {
                        "summary": "Недействительный токен",
                        "value": {"detail": "Не удалось проверить учетные данные"}
                    },
                    "expired_token": {
                        "summary": "Истекший токен",
                        "value": {"detail": "Срок действия токена истек"}
                    }
                }
            }
        }
    }
}

get_current_user_description = """
Получение информации о текущем пользователе.

Требует авторизации через заголовок:
Authorization: Bearer <access_token>

Возвращает полную информацию о текущем пользователе, включая:
- ID
- Email
- Полное имя
- Роль
- Статус активности
- Даты создания и обновления
"""

update_user_description = """
Обновление информации о текущем пользователе.

Требует авторизации через заголовок:
Authorization: Bearer <access_token>

Для обычных пользователей (role=user):
- Можно изменять только full_name, email и password
- Все поля опциональные
- При попытке изменить role или is_active вернется ошибка 403

Для администраторов (role=admin):
- Доступны все поля для изменения
- Все поля опциональные
- Можно менять роли и статус активности пользователей

Проверки при обновлении:
- Email должен быть уникальным
- Пароль должен соответствовать требованиям безопасности
- Имя должно быть от 2 до 50 символов
"""

delete_user_description = """
Удаление текущего пользователя.

Требует авторизации через заголовок:
Authorization: Bearer <access_token>

При удалении:
- Все сессии пользователя удаляются
- Все связанные данные удаляются
""" 