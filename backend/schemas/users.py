from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from services.roles import UserRole

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email пользователя")
    full_name: str = Field(..., description="Полное имя пользователя")
    is_active: bool = Field(default=True, description="Статус активности пользователя")
    role: UserRole = Field(default=UserRole.USER, description="Роль пользователя")

class UserResponse(UserBase):
    id: int = Field(..., description="Уникальный идентификатор пользователя")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обновления")

    class Config:
        json_schema_extra = {
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

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, description="Новое имя пользователя")
    email: Optional[EmailStr] = Field(None, description="Новый email")
    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=64,
        description="Новый пароль (если требуется изменить)"
    )
    role: Optional[UserRole] = Field(None, description="Новая роль пользователя (только для админов)") 