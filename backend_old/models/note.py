from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, relationship
from database import Base
from typing import Optional
import datetime

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    plant_id = Column(Integer, ForeignKey("plants.id", ondelete="CASCADE"), nullable=True)
    day = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())

    # Связь с растением
    plant = relationship("Plant", back_populates="notes")

    @classmethod
    def create(cls, db: Session, title: str, content: Optional[str] = None, 
               plant_id: Optional[int] = None, day: Optional[datetime.date] = None):
        """Создать новую заметку"""
        if not plant_id and not day:
            raise ValueError("Заметка должна быть привязана к растению или дню")
            
        db_note = cls(
            title=title,
            content=content,
            plant_id=plant_id,
            day=day
        )
        
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        
        return db_note
    
    @classmethod
    def get_by_id(cls, db: Session, note_id: int):
        """Получить заметку по ID"""
        return db.query(cls).filter(cls.id == note_id).first()
    
    @classmethod
    def get_plant_notes(cls, db: Session, plant_id: int):
        """Получить все заметки для растения"""
        return db.query(cls).filter(cls.plant_id == plant_id).all()
    
    @classmethod
    def get_day_notes(cls, db: Session, day: datetime.date):
        """Получить все заметки для конкретного дня"""
        return db.query(cls).filter(cls.day == day).all()
    
    @classmethod
    def get_user_day_notes(cls, db: Session, user_id: int, day: datetime.date):
        """Получить все заметки пользователя за конкретный день"""
        return db.query(cls).join(cls.plant).filter(
            cls.day == day, 
            cls.plant.has(user_id=user_id)
        ).all()
    
    def update(self, db: Session, **kwargs):
        """Обновить данные заметки"""
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key):
                setattr(self, key, value)
        
        self.updated_at = func.now()
        db.commit()
        db.refresh(self)
        return self
    
    def delete(self, db: Session):
        """Удалить заметку"""
        db.delete(self)
        db.commit()
        return {"message": "Заметка успешно удалена"} 