from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Session
from database import Base
from datetime import datetime, UTC
import sqlalchemy as sa

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plant_id = Column(Integer, ForeignKey("plants.id", ondelete="CASCADE"), nullable=True)
    day = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=sa.func.now())
    updated_at = Column(DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())

    user = relationship("User", back_populates="notes")
    plant = relationship("Plant", back_populates="notes")

    @classmethod
    def create(cls, db: Session, title: str, text: str, user_id: int, plant_id: int = None, day: datetime = None):
        db_note = cls(title=title, text=text, user_id=user_id, plant_id=plant_id, day=day)
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note
    
    @classmethod
    def get_by_id(cls, db: Session, id: int):
        return db.query(cls).filter(cls.id == id).first()
    
    @classmethod
    def get_all(cls, db: Session, user_id: int, plant_id: int = None):
        query = db.query(cls).filter(cls.user_id == user_id)
        if plant_id:
            query = query.filter(cls.plant_id == plant_id)
        return query.all()
    
    @classmethod
    def update(cls, db: Session, id: int, **kwargs):
        db_note = db.query(cls).filter(cls.id == id).first()
        for key, value in kwargs.items():
            if key not in [attr.name for attr in cls.__table__.columns]:
                continue
            setattr(db_note, key, value)
        db.commit()
        db.refresh(db_note)
        return db_note
    
    @classmethod
    def delete(cls, db: Session, id: int):
        db_note = db.query(cls).filter(cls.id == id).first()
        db.delete(db_note)
        db.commit()
        return True

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "user_id": self.user_id,
            "plant_id": self.plant_id,
            "day": self.day,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }