from fastapi import status

# Подробные описания эндпоинтов
get_sessions_description = """
Получить список всех активных сессий текущего пользователя.

Требует авторизации через заголовок:
Authorization: Bearer <access_token>

Возвращает:
1. Общее количество активных сессий (total)
2. Список сессий (sessions), каждая содержит:
   - id: Уникальный идентификатор сессии
   - is_current: Признак текущей сессии (true для сессии, с которой сделан запрос)
   - user_agent: Информация о браузере
   - ip_address: IP-адрес, с которого создана сессия
   - device_info: Подробная информация об устройстве
     * browser: Информация о браузере (family, version)
     * os: Информация об ОС (family, version)
     * device: Информация об устройстве (family, brand, model)
     * is_mobile: Мобильное устройство
     * is_tablet: Планшет
     * is_pc: Персональный компьютер
     * is_bot: Бот/Краулер
   - is_active: Статус активности сессии
   - created_at: Дата и время создания
   - updated_at: Дата и время последнего обновления

Определение текущей сессии:
- Поле is_current=true указывает на сессию, с которой выполнен текущий запрос
- Текущая сессия определяется по access_token из заголовка Authorization
- При завершении сессий текущая сессия не будет удалена
- Рекомендуется сохранять ID текущей сессии на фронтенде для быстрой фильтрации

Возможные ошибки:
- 401 UNAUTHORIZED:
  * Отсутствует токен авторизации
  * Недействительный токен
  * Срок действия токена истек
- 403 FORBIDDEN:
  * Недостаточно прав для просмотра сессий
- 422 UNPROCESSABLE_ENTITY:
  * Неверный формат токена
"""

terminate_session_description = """
Завершить указанную сессию пользователя.

Требует авторизации через заголовок:
Authorization: Bearer <access_token>

Входные данные:
- session_id: ID сессии для завершения (в URL)

Особенности:
- Пользователь может завершить только свои собственные сессии
- После завершения сессия деактивируется
- Все связанные токены становятся недействительными
- Требуется повторная авторизация с этого устройства

Возвращает:
- Сообщение об успешном завершении
- Информацию о завершенной сессии

Возможные ошибки:
- 401 UNAUTHORIZED:
  * Отсутствует токен авторизации
  * Недействительный токен
  * Срок действия токена истек
- 403 FORBIDDEN:
  * Попытка завершить чужую сессию
- 404 NOT_FOUND:
  * Сессия не найдена
  * Сессия не принадлежит текущему пользователю
- 422 UNPROCESSABLE_ENTITY:
  * Неверный формат ID сессии
"""

terminate_all_sessions_description = """
Завершить все активные сессии текущего пользователя, кроме текущей.

Требует авторизации через заголовок:
Authorization: Bearer <access_token>

Особенности:
- Текущая сессия остается активной
- Все остальные сессии деактивируются
- Пользователь будет разлогинен на всех других устройствах
- Требуется повторная авторизация на других устройствах

Сценарии использования:
- Подозрение на компрометацию учетной записи
- Выход со всех устройств кроме текущего
- Принудительное завершение всех старых сессий

Возможные ошибки:
- 401 UNAUTHORIZED:
  * Отсутствует токен авторизации
  * Недействительный токен
  * Срок действия токена истек
- 403 FORBIDDEN:
  * Недостаточно прав для завершения сессий
- 422 UNPROCESSABLE_ENTITY:
  * Неверный формат токена
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

# Подробные описания ответов
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
                            "is_current": "true",
                            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                            "ip_address": "192.168.1.1",
                            "device_info": {
                                "browser": {
                                    "family": "Chrome",
                                    "version": "120.0.0"
                                },
                                "os": {
                                    "family": "Windows",
                                    "version": "10"
                                },
                                "device": {
                                    "family": "Other",
                                    "brand": None,
                                    "model": None
                                },
                                "is_mobile": False,
                                "is_pc": True,
                                "is_bot": False,
                                "is_tablet": False
                            },
                            "is_active": True,
                            "created_at": "2024-02-19T12:00:00",
                            "updated_at": "2024-02-19T12:30:00"
                        },
                        {
                            "id": 2,
                            "is_current": "false",
                            "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)",
                            "ip_address": "192.168.1.2",
                            "device_info": {
                                "browser": {
                                    "family": "Mobile Safari",
                                    "version": "16.0"
                                },
                                "os": {
                                    "family": "iOS",
                                    "version": "16.0"
                                },
                                "device": {
                                    "family": "iPhone",
                                    "brand": "Apple",
                                    "model": "iPhone"
                                },
                                "is_mobile": True,
                                "is_pc": False,
                                "is_bot": False,
                                "is_tablet": False
                            },
                            "is_active": True,
                            "created_at": "2024-02-19T14:00:00",
                            "updated_at": "2024-02-19T14:30:00"
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
                "example": {
                    "detail": "Недостаточно прав для просмотра сессий"
                }
            }
        }
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "Ошибка валидации",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Неверный формат токена"
                }
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
                        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                        "ip_address": "192.168.1.1",
                        "device_info": {
                            "browser": {
                                "family": "Chrome",
                                "version": "120.0.0"
                            },
                            "os": {
                                "family": "Windows",
                                "version": "10"
                            },
                            "device": {
                                "family": "Other",
                                "brand": None,
                                "model": None
                            },
                            "is_mobile": False,
                            "is_pc": True,
                            "is_bot": False,
                            "is_tablet": False
                        },
                        "is_active": False,
                        "created_at": "2024-02-19T12:00:00",
                        "updated_at": "2024-02-19T15:30:00"
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
                "example": {
                    "detail": "Попытка завершить чужую сессию"
                }
            }
        }
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Сессия не найдена",
        "content": {
            "application/json": {
                "examples": {
                    "not_found": {
                        "summary": "Сессия не существует",
                        "value": {
                            "detail": "Сессия не найдена"
                        }
                    },
                    "not_owned": {
                        "summary": "Сессия принадлежит другому пользователю",
                        "value": {
                            "detail": "Сессия не найдена или не принадлежит текущему пользователю"
                        }
                    }
                }
            }
        }
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "Ошибка валидации",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Неверный формат ID сессии"
                }
            }
        }
    }
}

terminate_all_sessions_responses = {
    status.HTTP_200_OK: {
        "description": "Сессии успешно завершены",
        "content": {
            "application/json": {
                "examples": {
                    "all_except_current": {
                        "summary": "Завершены все сессии кроме текущей",
                        "value": {
                            "message": "Все остальные сессии успешно завершены"
                        }
                    },
                    "all_sessions": {
                        "summary": "Завершены все сессии",
                        "value": {
                            "message": "Все сессии успешно завершены"
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
                "example": {
                    "detail": "Недостаточно прав для завершения сессий"
                }
            }
        }
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "Ошибка валидации",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Неверный формат токена"
                }
            }
        }
    }
}
