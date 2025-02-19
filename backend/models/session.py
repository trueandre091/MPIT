from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import Session as DbSession, relationship
from database import Base
from datetime import datetime, timedelta, UTC
from typing import Optional

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    refresh_token = Column(String, unique=True, index=True)
    access_token = Column(String)
    user_agent = Column(String)
    ip_address = Column(String)
    device_info = Column(JSON)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=False))
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())

    # Связь с пользователем
    user = relationship("User", back_populates="sessions")

    @classmethod
    def create(cls, db: DbSession, user_id: int, refresh_token: str, access_token: str,
               user_agent: str, ip_address: str, device_info: dict,
               expires_in_days: int = 7) -> "Session":
        """
        Создать новую сессию
        """
        session = cls(
            user_id=user_id,
            refresh_token=refresh_token,
            access_token=access_token,
            user_agent=user_agent,
            ip_address=ip_address,
            device_info=device_info,
            expires_at=datetime.now(UTC) + timedelta(days=expires_in_days)
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @classmethod
    def get_by_refresh_token(cls, db: DbSession, refresh_token: str) -> Optional["Session"]:
        """
        Получить сессию по refresh token
        """
        session = db.query(cls).filter(
            cls.refresh_token == refresh_token,
            cls.is_active == True
        ).first()

        # Если сессия найдена, но срок её действия истек - удаляем её
        if session and session.expires_at <= datetime.now(UTC):
            db.delete(session)
            db.commit()
            return None

        return session

    @classmethod
    def get_user_sessions(cls, db: DbSession, user_id: int) -> list["Session"]:
        """
        Получить все активные сессии пользователя
        """
        return db.query(cls).filter(
            cls.user_id == user_id,
            cls.is_active == True,
            cls.expires_at > datetime.now(UTC)
        ).all()

    def deactivate(self, db: DbSession):
        """
        Деактивировать сессию
        """
        self.is_active = False
        db.commit()
        db.refresh(self)

    @classmethod
    def deactivate_all_user_sessions(cls, db: DbSession, user_id: int, except_token: Optional[str] = None):
        """
        Удалить все сессии пользователя (кроме указанной)
        """
        query = db.query(cls).filter(
            cls.user_id == user_id
        )
        if except_token:
            query = query.filter(cls.refresh_token != except_token)
        
        # Получаем все сессии для удаления
        sessions = query.all()
        for session in sessions:
            db.delete(session)
        db.commit()

    @classmethod
    def cleanup_expired_sessions(cls, db: DbSession):
        """
        Удалить все истекшие сессии
        """
        sessions = db.query(cls).filter(
            cls.expires_at <= datetime.now(UTC)
        ).all()
        for session in sessions:
            db.delete(session)
        db.commit()

    def update_tokens(self, db: DbSession, new_access_token: str, new_refresh_token: str):
        """
        Обновить токены в существующей сессии
        """
        self.access_token = new_access_token
        self.refresh_token = new_refresh_token
        self.updated_at = datetime.now(UTC)
        db.commit()
        db.refresh(self)
        return self

    def delete(self, db: DbSession):
        """
        Удалить сессию
        """
        db.delete(self)
        db.commit() 