from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, Session
from database import Base
from datetime import datetime, UTC

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now(UTC))
