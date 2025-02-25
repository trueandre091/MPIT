from pydantic import BaseModel, EmailStr, Field, validator, ValidationError
from typing import Optional, List, Dict
from datetime import datetime
from services.roles import UserRole

class PasswordError(Exception):
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__("Ошибки валидации пароля")

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
    """
    Схема обновления пользователя.
    
    Для обычных пользователей (role=user):
    - Можно изменять только full_name, email и password
    - Все поля опциональные
    
    Для администраторов (role=admin):
    - Доступны все поля для изменения
    - Все поля опциональные
    """
    full_name: Optional[str] = Field(
        None, 
        min_length=2,
        max_length=50,
        description="Новое имя пользователя",
        examples=["Иван Иванов"]
    )
    email: Optional[EmailStr] = Field(
        None, 
        description="Новый email",
        examples=["new.email@example.com"]
    )
    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=64,
        description="Новый пароль (если требуется изменить)",
        examples=["NewPassword123!"]
    )
    # Поля доступные только для администраторов
    role: Optional[UserRole] = Field(
        None, 
        description="Новая роль пользователя (только для админов)",
        examples=["admin", "user"]
    )
    is_active: Optional[bool] = Field(
        None, 
        description="Статус активности (только для админов)",
        examples=[True, False]
    )

    @validator('full_name')
    def validate_full_name(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError("Имя не может быть пустым")
            
            v = v.strip()
            errors = []
            
            if len(v) < 2:
                errors.append("Имя должно содержать минимум 2 символа")
            if len(v) > 50:
                errors.append("Имя не может быть длиннее 50 символов")
            if not all(c.isalpha() or c.isspace() for c in v):
                errors.append("Имя может содержать только буквы и пробелы")
            
            if errors:
                raise ValueError({"field": "full_name", "errors": errors})
            
            return v
        return v

    @validator('password')
    def validate_password(cls, v):
        if v is not None:
            errors = []
            
            if len(v) < 8:
                errors.append("Минимальная длина пароля - 8 символов")
            if len(v) > 64:
                errors.append("Максимальная длина пароля - 64 символа")
            if not any(c.isupper() for c in v):
                errors.append("Пароль должен содержать хотя бы одну заглавную букву (A-Z)")
            if not any(c.islower() for c in v):
                errors.append("Пароль должен содержать хотя бы одну строчную букву (a-z)")
            if not any(c.isdigit() for c in v):
                errors.append("Пароль должен содержать хотя бы одну цифру (0-9)")
            if not any(c in "!@#$%^&*(),.?\":{}|<>" for c in v):
                errors.append("Пароль должен содержать хотя бы один специальный символ (!@#$%^&*(),.?\":{}|<>)")
            
            if errors:
                raise ValueError({"field": "password", "errors": errors})
            
            return v
        return v

    @validator('email')
    def validate_email(cls, v):
        if v is not None:
            errors = []
            
            if not v:
                errors.append("Email не может быть пустым")
            elif '@' not in v:
                errors.append("Email должен содержать символ @")
            elif '.' not in v:
                errors.append("Email должен содержать доменную часть")
            elif len(v) > 255:
                errors.append("Email не может быть длиннее 255 символов")
            
            if errors:
                raise ValueError({"field": "email", "errors": errors})
            
            return v
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "full_name": "Иван Иванов",
                    "email": "new.email@example.com",
                    "password": "NewPassword123!"
                },
                {
                    "full_name": "Иван Иванов",
                    "email": "new.email@example.com",
                    "password": "NewPassword123!",
                    "role": "admin",
                    "is_active": True
                }
            ]
        }
    } 