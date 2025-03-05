from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, Session
from database import Base
from datetime import datetime, UTC
import bcrypt

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    @classmethod
    def create(cls, db: Session, email: str, password: str, name: str):
        db_user = cls(email=email, password=cls._hash_password(password), name=name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @classmethod
    def get_by_email(cls, db: Session, email: str):
        return db.query(cls).filter(cls.email == email).first()
    
    @classmethod
    def get_by_id(cls, db: Session, id: int):
        return db.query(cls).filter(cls.id == id).first()
    
    @staticmethod
    def _hash_password(password: str):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def _check_password(password: str, hashed_password: str):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @classmethod
    def update(cls, db: Session, id: int, **kwargs):
        db_user = db.query(cls).filter(cls.id == id).first()
        for key, value in kwargs.items():
            if key not in [attr.name for attr in cls.__table__.columns]:
                continue
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    


    
    
    
    
    
    
    
    
