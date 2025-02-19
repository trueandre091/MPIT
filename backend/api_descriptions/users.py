get_current_user_responses = {
    200: {
        "description": "Успешное получение данных пользователя",
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
    401: {
        "description": "Не авторизован",
        "content": {
            "application/json": {
                "example": {"detail": "Not authenticated"}
            }
        }
    }
}

update_user_responses = {
    200: {
        "description": "Успешное обновление данных",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "email": "updated@example.com",
                    "full_name": "Петр Петров",
                    "is_active": True,
                    "role": "user",
                    "created_at": "2024-02-19T12:00:00",
                    "updated_at": "2024-02-19T12:00:00"
                }
            }
        }
    },
    401: {"description": "Не авторизован"},
    400: {"description": "Некорректные данные"},
    422: {
        "description": "Ошибка валидации",
        "content": {
            "application/json": {
                "example": {"detail": "Invalid email format"}
            }
        }
    }
}

delete_user_responses = {
    200: {
        "description": "Пользователь успешно удален",
        "content": {
            "application/json": {
                "example": {"message": "Пользователь успешно удален"}
            }
        }
    },
    401: {"description": "Не авторизован"},
    404: {"description": "Пользователь не найден"}
}

get_current_user_description = """
Получение информации о текущем пользователе.

Требует авторизации через Bearer token.

Returns:
    UserResponse: Полная информация о текущем пользователе
"""

update_user_description = """
Обновление информации о текущем пользователе.

Требует авторизации через Bearer token.

Параметры:
- **full_name**: Новое имя пользователя (опционально)
- **email**: Новый email (опционально)
- **password**: Новый пароль (опционально)
- **role**: Новая роль пользователя (только для администраторов)

Returns:
    UserResponse: Обновленная информация о пользователе
"""

delete_user_description = """
Удаление текущего пользователя.

Требует авторизации через Bearer token.
Это действие необратимо!

Returns:
    dict: Сообщение об успешном удалении
""" 