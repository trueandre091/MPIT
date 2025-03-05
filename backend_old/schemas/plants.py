from pydantic import BaseModel, EmailStr, Field, validator, ValidationError
from typing import Optional, List, Dict
from datetime import datetime

class PlantBase(BaseModel):
    name: str = Field(..., description="Название растения")
    species: Optional[str] = Field(None, description="Вид растения")
    description: Optional[str] = Field(None, description="Описание растения")
    care_plan: Optional[Dict] = Field(None, description="План ухода за растением")
    image_url: Optional[str] = Field(None, description="URL изображения растения")
    
class PlantCreate(PlantBase):
    pass

class PlantUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название растения")
    species: Optional[str] = Field(None, description="Вид растения")
    description: Optional[str] = Field(None, description="Описание растения")

class PlantResponse(PlantBase):
    id: int
    user_id: int
    image_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Фикус",
                "species": "Ficus elastica",
                "description": "Мой любимый фикус",
                "user_id": 1,
                "image_path": "/static/plant_images/plant_1_123e4567-e89b-12d3-a456-426614174000.jpg",
                "created_at": "2023-01-01T12:00:00",
                "updated_at": "2023-01-01T12:00:00"
            }
        }

    


