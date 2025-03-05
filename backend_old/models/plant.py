from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, relationship
from database import Base
from typing import Optional, List
import os
import uuid
import shutil
from fastapi import UploadFile

class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    image_path = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())

    # Связь с пользователем
    user = relationship("User", back_populates="plants")
    
    # Связь с заметками
    notes = relationship("Note", back_populates="plant", cascade="all, delete-orphan")

    @classmethod
    async def create(cls, db: Session, user_id: int, name: str, species: Optional[str] = None, 
                    description: Optional[str] = None, image: Optional[UploadFile] = None):
        """Создать новое растение"""
        # Создаем запись в БД
        db_plant = cls(
            name=name,
            species=species,
            description=description,
            user_id=user_id
        )
        
        db.add(db_plant)
        db.commit()
        db.refresh(db_plant)
        
        # Если есть изображение, сохраняем его
        if image:
            await cls.save_image(db, db_plant.id, image)
        
        return db_plant
    
    @classmethod
    async def save_image(cls, db: Session, plant_id: int, image: UploadFile):
        """Сохранить изображение для растения"""
        # Получаем растение
        plant = db.query(cls).filter(cls.id == plant_id).first()
        if not plant:
            return None
        
        # Создаем директорию для хранения изображений, если её нет
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "plant_images")
        os.makedirs(upload_dir, exist_ok=True)
        
        # Генерируем уникальное имя файла
        file_extension = os.path.splitext(image.filename)[1]
        image_name = f"plant_{plant_id}_{uuid.uuid4()}{file_extension}"
        image_path = os.path.join(upload_dir, image_name)
        
        # Сохраняем изображение
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        # Если у растения уже было изображение, удаляем его
        if plant.image_path and os.path.exists(plant.image_path):
            os.remove(plant.image_path)
        
        # Обновляем путь к изображению в БД
        plant.image_path = image_path
        db.commit()
        db.refresh(plant)
        
        return plant
    
    @classmethod
    def get_by_id(cls, db: Session, plant_id: int):
        """Получить растение по ID"""
        return db.query(cls).filter(cls.id == plant_id).first()
    
    @classmethod
    def get_user_plants(cls, db: Session, user_id: int):
        """Получить все растения пользователя"""
        return db.query(cls).filter(cls.user_id == user_id).all()
    
    def update(self, db: Session, **kwargs):
        """Обновить данные растения"""
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key) and key != 'image_path':
                setattr(self, key, value)
        
        self.updated_at = func.now()
        db.commit()
        db.refresh(self)
        return self
    
    def delete(self, db: Session):
        """Удалить растение"""
        # Удаляем изображение, если оно есть
        if self.image_path and os.path.exists(self.image_path):
            os.remove(self.image_path)
        
        db.delete(self)
        db.commit()
        return {"message": "Растение успешно удалено"}
