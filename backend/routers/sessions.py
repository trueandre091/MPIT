from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.session import Session as DbSession
from models.user import User
from schemas.auth import SessionInfo, SessionList, SessionResponse, Token
from routers.auth import get_current_user
from services.token import token_service
from api_descriptions.sessions import (
    get_sessions_description,
    terminate_session_description,
    terminate_all_sessions_description,
    refresh_session_description,
    get_sessions_responses,
    terminate_session_responses,
    terminate_all_sessions_responses,
    refresh_session_responses
)

router = APIRouter()

@router.get(
    "/sessions/me",
    response_model=SessionList,
    description=get_sessions_description,
    responses=get_sessions_responses
)
async def get_my_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить список всех активных сессий текущего пользователя
    """
    sessions = DbSession.get_user_sessions(db, current_user.id)
    return {
        "total": len(sessions),
        "sessions": sessions
    }

@router.delete(
    "/sessions/{session_id}",
    response_model=SessionResponse,
    description=terminate_session_description,
    responses=terminate_session_responses
)
async def terminate_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Завершить указанную сессию.
    Пользователь может завершить только свои сессии.
    """
    session = db.query(DbSession).filter(
        DbSession.id == session_id,
        DbSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сессия не найдена или не принадлежит текущему пользователю"
        )
    
    session.deactivate(db)
    return {
        "message": "Сессия успешно завершена",
        "session": session
    }

@router.delete(
    "/sessions/me/all",
    response_model=SessionResponse,
    description=terminate_all_sessions_description,
    responses=terminate_all_sessions_responses
)
async def terminate_all_sessions(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Завершить все сессии текущего пользователя, кроме текущей
    """
    # Получаем текущий refresh token из сессии
    current_session = db.query(DbSession).filter(
        DbSession.user_id == current_user.id,
        DbSession.is_active == True,
        DbSession.access_token == request.headers.get("authorization").split()[1]
    ).first()

    if current_session:
        DbSession.deactivate_all_user_sessions(
            db, 
            current_user.id, 
            except_token=current_session.refresh_token
        )
        message = "Все остальные сессии успешно завершены"
    else:
        DbSession.deactivate_all_user_sessions(db, current_user.id)
        message = "Все сессии успешно завершены"

    return {
        "message": message
    }

@router.post(
    "/sessions/refresh",
    response_model=Token,
    description=refresh_session_description,
    responses=refresh_session_responses,
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
async def refresh_session(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Обновить сессию, используя refresh token.
    Создает новую пару access/refresh токенов и обновляет информацию о сессии.
    
    Refresh token должен быть передан в заголовке X-Refresh-Token.
    """
    # Получаем refresh token из заголовка
    refresh_token = request.headers.get("x-refresh-token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token не предоставлен"
        )

    # Находим сессию по refresh token
    session = DbSession.get_by_refresh_token(db, refresh_token)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный refresh token"
        )

    # Получаем пользователя
    user = User.get_by_id(db, session.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
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
            "is_active": user.is_active,
            "role": user.role
        }
    } 