from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

class NoteBase(BaseModel):
    title: str = Field(..., description="Заголовок заметки")
    content: Optional[str] = Field(None, description="Содержание заметки")
    plant_id: Optional[int] = Field(None, description="ID растения, к которому относится заметка")
    day: Optional[date] = Field(None, description="Дата, к которой относится заметка")

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Заголовок заметки")
    content: Optional[str] = Field(None, description="Содержание заметки")
    plant_id: Optional[int] = Field(None, description="ID растения, к которому относится заметка")
    day: Optional[date] = Field(None, description="Дата, к которой относится заметка")

class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Полив",
                "content": "Сегодня полил растение",
                "plant_id": 1,
                "day": "2023-01-01",
                "created_at": "2023-01-01T12:00:00",
                "updated_at": "2023-01-01T12:00:00"
            }
        } 