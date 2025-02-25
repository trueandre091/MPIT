from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.session import Session as DbSession
from models.user import User
from schemas.auth import SessionInfo, SessionList, SessionResponse
from routers.auth import get_current_user
from api_descriptions.sessions import (
    get_sessions_description,
    terminate_session_description,
    terminate_all_sessions_description,
    get_sessions_responses,
    terminate_session_responses,
    terminate_all_sessions_responses
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