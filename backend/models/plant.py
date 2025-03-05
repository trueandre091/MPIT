from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Session
from database import Base
import sqlalchemy as sa
from services.image_service import get_image_url

class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False, server_default="")
    image = Column(String, nullable=False, server_default="")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=sa.func.now())
    updated_at = Column(DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())

    user = relationship("User", back_populates="plants")
    notes = relationship("Note", back_populates="plant", cascade="all, delete-orphan")

    def to_dict(self, full: bool = False):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": get_image_url(self.id, self.image) if self.image else "",
            "user_id": self.user_id,
            "notes": [note.to_dict() for note in self.notes] if full else [note.id for note in self.notes],
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def create(cls, db: Session, name: str, user_id: int, description: str = "", image: str = ""):
        db_plant = cls(name=name, description=description, image=image, user_id=user_id)
        db.add(db_plant)
        db.commit()
        db.refresh(db_plant)
        return db_plant
    
    @classmethod
    def get_by_id(cls, db: Session, id: int):
        return db.query(cls).filter(cls.id == id).first()
    
    @classmethod
    def get_all(cls, db: Session):
        return db.query(cls).all()
    
    @classmethod
    def get_all_by_user_id(cls, db: Session, user_id: int):
        return db.query(cls).filter(cls.user_id == user_id).all()
    
    @classmethod
    def update(cls, db: Session, id: int, **kwargs):
        db_plant = db.query(cls).filter(cls.id == id).first()
        for key, value in kwargs.items():
            if key not in [attr.name for attr in cls.__table__.columns]:
                continue
            setattr(db_plant, key, value)
        db.commit()
        db.refresh(db_plant)
        return db_plant
    
    @classmethod
    def delete(cls, db: Session, id: int):
        db_plant = db.query(cls).filter(cls.id == id).first()
        db.delete(db_plant)
        db.commit()
        return True

