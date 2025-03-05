from sqlalchemy import Boolean, Column, Integer, String, DateTime, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, relationship
from database import Base
from schemas.auth import UserCreate
from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    role = Column(String, default="user")
    plants_id = Column(ARRAY(Integer))
    notes_id = Column(ARRAY(Integer))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())

    # Связь с сессиями
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    
    # Связь с растениями - используем строковое имя для отложенной загрузки
    plants = relationship("Plant", back_populates="user", cascade="all, delete-orphan")

    @classmethod
    def get_by_email(cls, db: Session, email: str):
        """Получить пользователя по email"""
        return db.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_by_id(cls, db: Session, user_id: int):
        """Получить пользователя по ID"""
        return db.query(cls).filter(cls.id == user_id).first()

    @classmethod
    def create(cls, db: Session, user_data: UserCreate, hashed_password: str):
        """Создать нового пользователя"""
        db_user = cls(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @classmethod
    def authenticate(cls, db: Session, email: str, password: str):
        """Аутентифицировать пользователя"""
        user = cls.get_by_email(db, email)
        if not user:
            return None
        if not cls.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Проверить пароль"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Получить хеш пароля"""
        return pwd_context.hash(password)

    def update(self, db: Session, **kwargs):
        """Обновить данные пользователя"""
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key):
                if key == 'email' and value != self.email:
                    # Проверяем, не занят ли email другим пользователем
                    existing_user = db.query(User).filter(
                        User.email == value,
                        User.id != self.id
                    ).first()
                    if existing_user:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered"
                        )
                setattr(self, key, value)
        
        self.updated_at = func.now()
        db.commit()
        db.refresh(self)
        return self

    def delete(self, db: Session):
        """Удалить пользователя"""
        db.delete(self)
        db.commit()
        return {"message": "Пользователь успешно удален"} 