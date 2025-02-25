from fastapi import APIRouter, HTTPException, Depends, status, Security
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from schemas.users import UserResponse, UserUpdate
from api_descriptions.users import (
    get_current_user_responses,
    update_user_responses,
    delete_user_responses,
    get_current_user_description,
    update_user_description,
    delete_user_description
)
from models.user import User
from database import get_db
from routers.auth import get_current_user
from services.roles import admin_required, UserRole

router = APIRouter()

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True

@router.get(
    "/users/me",
    response_model=UserResponse,
    responses=get_current_user_responses,
    description=get_current_user_description,
    dependencies=[Security(get_current_user)]
)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Получение информации о текущем пользователе.
    
    Требует авторизации через Bearer token.
    
    Returns:
        UserResponse: Полная информация о пользователе
    """
    return current_user

@router.get(
    "/users", 
    response_model=List[UserResponse],
    dependencies=[Security(admin_required)]
)
async def get_users(db: Session = Depends(get_db)):
    """
    Получить список всех пользователей
    
    Требует авторизации через Bearer token.
    Доступно только для администраторов.
    """
    return db.query(User).all()

@router.get(
    "/users/{user_id}", 
    response_model=UserResponse,
    dependencies=[Security(admin_required)]
)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Получить информацию о пользователе по ID
    
    Требует авторизации через Bearer token.
    Доступно только для администраторов.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user

@router.patch(
    "/users/me",
    response_model=UserResponse,
    responses=update_user_responses,
    description=update_user_description,
    dependencies=[Security(get_current_user)]
)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Обновление информации о текущем пользователе.
    
    Для обычных пользователей (role=user):
    - Можно изменять только full_name, email и password
    - Все поля опциональные
    
    Для администраторов (role=admin):
    - Доступны все поля для изменения
    - Все поля опциональные
    """
    # Получаем только заполненные поля
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Проверяем права доступа
    if current_user.role != UserRole.ADMIN:
        # Для обычных пользователей удаляем поля, которые они не могут изменять
        admin_fields = ['role', 'is_active']
        for field in admin_fields:
            if field in update_data:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Поле '{field}' может изменять только администратор"
                )
    
    # Проверяем email на уникальность
    if "email" in update_data and update_data["email"] != current_user.email:
        existing_user = db.query(User).filter(
            User.email == update_data["email"],
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Этот email уже используется"
            )
    
    # Хешируем пароль, если он был предоставлен
    if "password" in update_data:
        update_data["hashed_password"] = User.get_password_hash(update_data.pop("password"))
    
    try:
        # Обновляем пользователя
        updated_user = current_user.update(db, **update_data)
        return updated_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обновлении пользователя"
        )

@router.delete(
    "/users/me",
    responses=delete_user_responses,
    description=delete_user_description,
    dependencies=[Security(get_current_user)]
)
async def delete_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Удалить текущего пользователя
    
    Требует авторизации через Bearer token.
    """
    return current_user.delete(db)

@router.delete(
    "/users/{user_id}",
    dependencies=[Security(admin_required)]
)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Удалить пользователя по ID
    
    Требует авторизации через Bearer token.
    Доступно только для администраторов.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user.delete(db) 