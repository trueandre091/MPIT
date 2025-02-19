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

class Token(BaseModel):
    access_token: str = Field(..., description="JWT токен доступа")
    refresh_token: str = Field(..., description="Refresh токен для обновления access токена")
    token_type: str = Field(..., description="Тип токена (bearer)")
    user: UserResponse = Field(..., description="Информация о пользователе")

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

class UserCreate(UserAuth):
    full_name: str = Field(
        ..., 
        min_length=2,
        max_length=50,
        description="Полное имя пользователя (от 2 до 50 символов)",
        examples=["Иван Иванов"]
    )
    
    @validator('full_name')
    def full_name_validation(cls, v):
        if not re.match(r'^[а-яА-Яa-zA-Z\s]{2,50}$', v):
            raise ValueError(
                'Имя должно содержать:\n'
                '- Только буквы (русские или английские) и пробелы\n'
                '- Длину от 2 до 50 символов'
            )
        return ' '.join(v.split()) 