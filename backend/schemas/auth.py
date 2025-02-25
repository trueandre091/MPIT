from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, List
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
import re

class UserBase(BaseModel):
    email: EmailStr = Field(
        ..., 
        description="Email пользователя",
        examples=["user@example.com"]
    )
    full_name: str = Field(
        ..., 
        description="Полное имя пользователя",
        min_length=2,
        max_length=50,
        examples=["Иван Иванов"]
    )

class UserResponse(UserBase):
    id: int = Field(..., description="ID пользователя")
    is_active: bool = Field(default=True, description="Статус активности")
    role: str = Field(..., description="Роль пользователя")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обновления")

    model_config = {
        "json_schema_extra": {
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

class Token(BaseModel):
    access_token: str = Field(..., description="JWT токен доступа")
    refresh_token: str = Field(..., description="Refresh токен для обновления access токена")
    token_type: str = Field(..., description="Тип токена (bearer)")
    user: UserResponse = Field(..., description="Информация о пользователе")

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
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
    }

class TokenData(BaseModel):
    email: Optional[str] = None

class SessionInfo(BaseModel):
    id: int
    user_agent: str
    ip_address: str
    device_info: Dict
    is_active: bool
    created_at: datetime
    last_activity: datetime = Field(alias="updated_at")

    class Config:
        from_attributes = True

class SessionList(BaseModel):
    total: int
    sessions: List[SessionInfo]

class SessionResponse(BaseModel):
    message: str
    session: Optional[SessionInfo] = None

class UserAuth(BaseModel):
    email: EmailStr = Field(
        ..., 
        description="Email пользователя",
        examples=["user@example.com"]
    )
    password: str = Field(
        ..., 
        min_length=8,
        max_length=64,
        description="Пароль пользователя (от 8 до 64 символов)",
        examples=["Password123!"]
    )

    @validator('password')
    def password_validation(cls, v):
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,64}$', v):
            raise ValueError(
                'Пароль должен содержать:\n'
                '- Минимум 8 символов\n'
                '- Хотя бы одну заглавную букву (A-Z)\n'
                '- Хотя бы одну строчную букву (a-z)\n'
                '- Хотя бы одну цифру (0-9)\n'
                '- Хотя бы один специальный символ (@$!%*?&#)'
            )
        return v

class RegistrationForm(OAuth2PasswordRequestForm):
    full_name: str

    def __init__(self, username: str, password: str, full_name: str):
        super().__init__(username=username, password=password)
        self.full_name = full_name

    @validator('full_name')
    def full_name_validation(cls, v):
        if not re.match(r'^[а-яА-Яa-zA-Z\s]{2,50}$', v):
            raise ValueError(
                'Имя должно содержать только буквы и пробелы, '
                'длина от 2 до 50 символов'
            )
        return v

class UserCreate(BaseModel):
    email: EmailStr = Field(
        ..., 
        description="Email пользователя",
        examples=["user@example.com"]
    )
    password: str = Field(
        ..., 
        min_length=8,
        max_length=64,
        description="Пароль пользователя",
        examples=["Password123!"]
    )
    full_name: str = Field(
        ..., 
        min_length=2,
        max_length=50,
        description="Полное имя пользователя",
        examples=["Иван Иванов"]
    )
    
    @validator('full_name')
    def validate_full_name(cls, v):
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
        
        return ' '.join(v.split())

    @validator('password')
    def validate_password(cls, v):
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

    @validator('email')
    def validate_email(cls, v):
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

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "Password123!",
                "full_name": "Иван Иванов"
            }
        }
    }