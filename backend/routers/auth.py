from fastapi import APIRouter, HTTPException, Depends, status, Form, Request
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from schemas.auth import Token, TokenData, UserAuth, UserCreate
from api_descriptions.auth import (
    register_responses, 
    login_responses,
    register_description,
    login_description,
    refresh_description
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
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    
    # Проверяем, не занят ли email
    if User.get_by_email(db, email=username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
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
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "full_name": db_user.full_name,
            "role": db_user.role
        }
    }

@router.post(
    "/auth/login",
    response_model=Token,
    responses=login_responses,
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
        UserAuth.model_validate({"email": form_data.username, "password": form_data.password})
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid email format"
        )

    # Аутентифицируем пользователя
    user = User.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
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
            "role": user.role
        }
    }

@router.post(
    "/auth/logout",
    response_model=dict,
    description="Выход из системы"
)
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Выход из системы (удаление текущей сессии)
    """
    # Получаем текущую сессию по access token
    current_token = request.headers.get("authorization").split()[1]
    session = db.query(DbSession).filter(
        DbSession.user_id == current_user.id,
        DbSession.access_token == current_token,
        DbSession.is_active == True
    ).first()

    if session:
        session.delete(db)
        return {"message": "Успешный выход из системы"}
    
    return {"message": "Сессия уже была завершена"}

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Находим сессию по refresh token
    session = DbSession.get_by_refresh_token(db, refresh_token)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Сессия не найдена или истекла",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Получаем пользователя
    user = User.get_by_id(db, session.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
            headers={"WWW-Authenticate": "Bearer"}
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
            "role": user.role
        }
    }

@router.get("/auth/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Получение информации о текущем пользователе
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "role": current_user.role,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at
    } 