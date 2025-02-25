from fastapi import APIRouter, HTTPException, Depends, status, Form, Request
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from pydantic import ValidationError

from schemas.auth import Token, TokenData, UserAuth, UserCreate
from api_descriptions.auth import (
    register_responses, 
    login_responses,
    register_description,
    login_description,
    refresh_description,
    refresh_responses
)
from models.user import User
from database import get_db
from services.token import token_service
from services.token import TokenError
from models.session import Session as DbSession

load_dotenv()

router = APIRouter()

# Настройки безопасности
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Функции безопасности
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """
    Получение текущего пользователя из токена
    """
    try:
        token = credentials.credentials
        payload, error = token_service.verify_token(token, expected_type="access")
        
        if error:
            error_messages = {
                TokenError.EXPIRED: "Срок действия токена истек",
                TokenError.INVALID_TYPE: "Неверный тип токена",
                TokenError.INVALID_SIGNATURE: "Токен поврежден или подделан",
                TokenError.MALFORMED: "Неверный формат токена"
            }
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_messages.get(error, "Could not validate credentials"),
                headers={"WWW-Authenticate": "Bearer"}
            )
            
        # Получаем user_id из токена
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен не содержит идентификатора пользователя",
                headers={"WWW-Authenticate": "Bearer"}
            )
            
        # Получаем пользователя по ID (более эффективно, чем по email)
        user = User.get_by_id(db, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Дополнительная проверка email для безопасности
        if user.email != payload.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Данные пользователя не совпадают",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Проверка роли (если она изменилась)
        if user.role != payload.get("role"):
            # Если роль изменилась, можно либо выдать новый токен, либо отклонить запрос
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Роль пользователя была изменена. Требуется повторная авторизация",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return user
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка проверки токена",
            headers={"WWW-Authenticate": "Bearer"}
        )

# Эндпоинты
@router.post(
    "/auth/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    responses=register_responses,
    description=register_description
)
async def register(
    request: Request,
    username: str = Form(..., description="Email пользователя"),
    password: str = Form(..., description="Пароль пользователя"),
    full_name: str = Form(..., description="Полное имя пользователя"),
    db: Session = Depends(get_db)
):
    """
    Регистрация нового пользователя через форму
    
    Параметры формы:
    - **username**: Email пользователя (например, user@example.com)
    - **password**: Пароль (минимум 8 символов, должен содержать заглавные и строчные буквы, цифры и спецсимволы)
    - **full_name**: Полное имя пользователя (только буквы и пробелы, от 2 до 50 символов)
    """
    # Проверяем формат данных
    try:
        user_data = UserCreate(
            email=username,
            password=password,
            full_name=full_name
        )
    except ValidationError as e:
        errors = {}
        for error in e.errors():
            field = error["loc"][0]
            if isinstance(error["ctx"], dict) and "errors" in error["ctx"]:
                errors[field] = error["ctx"]["errors"]
            else:
                errors[field] = [error["msg"]]
        
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=errors
        )
    
    # Проверяем, не занят ли email
    if User.get_by_email(db, email=username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Этот email уже зарегистрирован"
        )
    
    # Создаем пользователя
    hashed_password = User.get_password_hash(password)
    db_user = User.create(db, user_data, hashed_password)
    
    # Создаем токены
    token_data = {
        "sub": db_user.email,
        "user_id": db_user.id,
        "role": db_user.role
    }
    access_token = token_service.create_access_token(token_data)
    refresh_token = token_service.create_refresh_token(token_data)

    # Создаем сессию
    user_agent = request.headers.get("user-agent", "")
    device_info = parse_user_agent(user_agent)
    
    session = DbSession(
        user_id=db_user.id,
        refresh_token=refresh_token,
        access_token=access_token,
        user_agent=user_agent,
        ip_address=request.client.host,
        device_info=device_info,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    # Возвращаем полную информацию о пользователе
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "full_name": db_user.full_name,
            "role": db_user.role,
            "is_active": db_user.is_active,
            "created_at": db_user.created_at,
            "updated_at": db_user.updated_at
        }
    }

@router.post(
    "/auth/login",
    response_model=Token,
    responses={
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
            "description": "Неверные учетные данные",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Неверный email или пароль"
                    }
                }
            }
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации данных",
            "content": {
                "application/json": {
                    "examples": {
                        "validation_error": {
                            "summary": "Ошибки валидации",
                            "value": {
                                "detail": {
                                    "email": ["Email должен содержать символ @"],
                                    "password": [
                                        "Минимальная длина пароля - 8 символов",
                                        "Пароль должен содержать хотя бы одну заглавную букву (A-Z)",
                                        "Пароль должен содержать хотя бы одну цифру (0-9)"
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Аккаунт заблокирован",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Аккаунт неактивен или заблокирован"
                    }
                }
            }
        }
    },
    description=login_description
)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Вход в систему
    """
    # Проверяем формат email
    try:
        UserAuth.model_validate({
            "email": form_data.username, 
            "password": form_data.password
        })
    except ValidationError as e:
        errors = {}
        for error in e.errors():
            field = error["loc"][0]
            if isinstance(error["ctx"], dict) and "errors" in error["ctx"]:
                errors[field] = error["ctx"]["errors"]
            else:
                errors[field] = [error["msg"]]
        
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=errors
        )

    # Получаем пользователя
    user = User.get_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )

    # Проверяем активность аккаунта
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Аккаунт неактивен или заблокирован"
        )

    # Проверяем пароль
    if not User.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    # Создаем токены
    token_data = {
        "sub": user.email,
        "user_id": user.id,
        "role": user.role
    }
    access_token = token_service.create_access_token(token_data)
    refresh_token = token_service.create_refresh_token(token_data)

    # Создаем сессию
    user_agent = request.headers.get("user-agent", "")
    device_info = parse_user_agent(user_agent)
    
    session = DbSession(
        user_id=user.id,
        refresh_token=refresh_token,
        access_token=access_token,
        user_agent=user_agent,
        ip_address=request.client.host,
        device_info=device_info,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
    }

@router.post(
    "/auth/logout",
    response_model=dict,
    description="Выход из системы (завершение текущей сессии)",
    responses={
        status.HTTP_200_OK: {
            "description": "Успешный выход",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Сессия завершена",
                            "value": {"message": "Успешный выход из системы"}
                        },
                        "already_logged_out": {
                            "summary": "Уже завершена",
                            "value": {"message": "Сессия уже была завершена"}
                        }
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Отсутствует токен",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Отсутствует токен авторизации"
                    }
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Срок действия токена истек",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Срок действия токена истек"
                    }
                }
            }
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Недействительный токен",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_signature": {
                            "summary": "Неверная подпись",
                            "value": {
                                "detail": "Токен поврежден или подделан"
                            }
                        },
                        "invalid_format": {
                            "summary": "Неверный формат",
                            "value": {
                                "detail": "Неверный формат токена"
                            }
                        },
                        "invalid_type": {
                            "summary": "Неверный тип",
                            "value": {
                                "detail": "Неверный тип токена (ожидается access)"
                            }
                        }
                    }
                }
            }
        }
    }
)
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Выход из системы (завершение текущей сессии)
    
    Требуется передать:
    - Действующий access token в заголовке Authorization
    
    При успешном выходе:
    - Текущая сессия деактивируется
    - Все связанные токены становятся недействительными
    """
    try:
        # Получаем токен из заголовка
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Отсутствует токен авторизации"
            )
        
        current_token = auth_header.split()[1]
        
        # Проверяем токен
        payload, error = token_service.verify_token(current_token, expected_type="access")
        if error:
            error_codes = {
                TokenError.EXPIRED: (status.HTTP_403_FORBIDDEN, "Срок действия токена истек"),
                TokenError.INVALID_TYPE: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Неверный тип токена (ожидается access)"),
                TokenError.INVALID_SIGNATURE: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Токен поврежден или подделан"),
                TokenError.MALFORMED: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Неверный формат токена")
            }
            status_code, detail = error_codes.get(error, (status.HTTP_422_UNPROCESSABLE_ENTITY, "Недействительный токен"))
            raise HTTPException(status_code=status_code, detail=detail)

        # Находим и деактивируем сессию
        session = db.query(DbSession).filter(
            DbSession.user_id == current_user.id,
            DbSession.access_token == current_token,
            DbSession.is_active == True
        ).first()

        if session:
            session.delete(db)
            return {"message": "Успешный выход из системы"}
        
        return {"message": "Сессия уже была завершена"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Ошибка при выходе из системы"
        )

def parse_user_agent(user_agent: str) -> dict:
    """Парсинг User-Agent для получения информации об устройстве"""
    import user_agents

    ua = user_agents.parse(user_agent)
    return {
        "browser": {
            "family": ua.browser.family,
            "version": ua.browser.version_string,
        },
        "os": {
            "family": ua.os.family,
            "version": ua.os.version_string,
        },
        "device": {
            "family": ua.device.family,
            "brand": ua.device.brand,
            "model": ua.device.model,
        },
        "is_mobile": ua.is_mobile,
        "is_tablet": ua.is_tablet,
        "is_pc": ua.is_pc,
        "is_bot": ua.is_bot
    }

@router.post(
    "/auth/refresh",
    response_model=Token,
    description=refresh_description,
    responses={
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
            "description": "Отсутствует токен",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Refresh token не предоставлен"
                    }
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Срок действия токена истек",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Срок действия токена истек"
                    }
                }
            }
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Недействительный токен",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_signature": {
                            "summary": "Неверная подпись",
                            "value": {
                                "detail": "Токен поврежден или подделан"
                            }
                        },
                        "invalid_format": {
                            "summary": "Неверный формат",
                            "value": {
                                "detail": "Неверный формат токена"
                            }
                        },
                        "invalid_type": {
                            "summary": "Неверный тип",
                            "value": {
                                "detail": "Неверный тип токена (ожидается refresh)"
                            }
                        }
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
    },
    openapi_extra={
        "parameters": [
            {
                "in": "header",
                "name": "X-Refresh-Token",
                "schema": {"type": "string"},
                "required": True,
                "description": "Refresh token для обновления сессии"
            }
        ]
    }
)
async def refresh_token(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Обновление токена с помощью refresh token
    
    Refresh token должен быть передан в заголовке X-Refresh-Token.
    """
    # Получаем refresh token из заголовка
    refresh_token = request.headers.get("x-refresh-token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token не предоставлен"
        )

    # Проверяем refresh token
    payload, error = token_service.verify_token(refresh_token, expected_type="refresh")
    if error:
        error_codes = {
            TokenError.EXPIRED: (status.HTTP_403_FORBIDDEN, "Срок действия токена истек"),
            TokenError.INVALID_TYPE: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Неверный тип токена (ожидается refresh)"),
            TokenError.INVALID_SIGNATURE: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Токен поврежден или подделан"),
            TokenError.MALFORMED: (status.HTTP_422_UNPROCESSABLE_ENTITY, "Неверный формат токена")
        }
        status_code, detail = error_codes.get(error, (status.HTTP_422_UNPROCESSABLE_ENTITY, "Недействительный токен"))
        raise HTTPException(status_code=status_code, detail=detail)

    # Находим сессию по refresh token
    session = DbSession.get_by_refresh_token(db, refresh_token)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Сессия не найдена или истекла"
        )

    # Получаем пользователя
    user = User.get_by_id(db, session.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    # Создаем новые токены
    token_data = {
        "sub": user.email,
        "user_id": user.id,
        "role": user.role
    }
    new_access_token = token_service.create_access_token(token_data)
    new_refresh_token = token_service.create_refresh_token(token_data)

    # Обновляем существующую сессию
    session.update_tokens(db, new_access_token, new_refresh_token)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
    } 

@router.get(
    "/auth/verify",
    status_code=status.HTTP_200_OK,
    description="Проверка валидности токена",
    responses={
        status.HTTP_200_OK: {
            "description": "Токен действителен",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Токен действителен"
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Токен недействителен",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Недействительный токен"
                    }
                }
            }
        }
    }
)
async def verify_token(current_user: User = Depends(get_current_user)):
    """
    Проверка валидности токена.
    
    Если токен действителен, возвращает 200 OK.
    Если токен недействителен, возвращает 401 Unauthorized.
    """
    return {"detail": "Токен действителен"}



