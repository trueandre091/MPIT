from fastapi import APIRouter, HTTPException, Depends, status, Form
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
from database import get_db
from sqlalchemy.orm import Session
from settings import get_settings

from services.auth_service import AuthService
from services.user_service import UserCreate

from models.user import User

settings = get_settings()
router = APIRouter()
auth_service = AuthService()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    user = UserCreate(email=email, password=password, name=name)

    if User.get_by_email(db, user.email):
        raise HTTPException(status_code=406, detail="User already exists")
    
    user = User.create(db, user.email, user.password, user.name)
    token = auth_service.create_token({"sub": str(user.id)})
    
    return {
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role
        }
    }


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = User.get_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        User.update(db, user.id, is_active=True)
    
    if not User._check_password(password, user.password):
        raise HTTPException(status_code=403, detail="Invalid password")
    
    token = auth_service.create_token({"sub": str(user.id)})
    return {
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role
        }
    }

@router.get("/me", status_code=status.HTTP_200_OK)
async def me(
    user: User = Depends(auth_service.verify_user),
    db: Session = Depends(get_db)
):
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role
        }
    }

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    user: User = Depends(auth_service.verify_user),
    db: Session = Depends(get_db)
):
    User.update(db, user.id, is_active=False)
    return {"detail": "Logged out"}








