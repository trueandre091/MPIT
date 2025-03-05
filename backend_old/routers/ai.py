from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from routers.auth import get_current_user
from services.ai_service import ai_service
import os
import uuid
from typing import Dict, List

router = APIRouter()

class PredictionResponse(BaseModel):
    predicted_class: str
    confidence: float
    probabilities: Dict[str, float]

@router.post(
    "/ai/classify-plant",
    response_model=PredictionResponse,
    description="Классификация растения по изображению",
    responses={
        status.HTTP_200_OK: {
            "description": "Успешная классификация",
            "content": {
                "application/json": {
                    "example": {
                        "predicted_class": "Томат",
                        "confidence": 0.95,
                        "probabilities": {
                            "Томат": 0.95,
                            "Огурец": 0.03,
                            "Перец": 0.02
                        }
                    }
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Ошибка при обработке запроса",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Модель не загружена"
                    }
                }
            }
        }
    }
)
async def classify_plant(
    file: UploadFile = File(..., description="Изображение растения для классификации"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Эндпоинт для классификации растений по изображению
    """
    try:
        # Создаем временную директорию для сохранения загруженных файлов, если её нет
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        
        # Генерируем уникальное имя файла
        file_extension = os.path.splitext(file.filename)[1]
        temp_file_name = f"{uuid.uuid4()}{file_extension}"
        temp_file_path = os.path.join(upload_dir, temp_file_name)
        
        # Сохраняем загруженный файл
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Получаем предсказание
        result = ai_service.predict(temp_file_path)
        
        # Удаляем временный файл
        os.remove(temp_file_path)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке запроса: {str(e)}")
