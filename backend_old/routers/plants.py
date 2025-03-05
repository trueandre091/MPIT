from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models.plant import Plant
from models.user import User
from schemas.plants import PlantCreate, PlantResponse, PlantUpdate
from routers.auth import get_current_user

router = APIRouter()

@router.post(
    "/plants",
    response_model=PlantResponse,
    status_code=status.HTTP_201_CREATED,
    description="Создать новое растение"
)
async def create_plant(
    name: str,
    species: Optional[str] = None,
    description: Optional[str] = None,
    image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать новое растение"""
    plant = await Plant.create(
        db=db,
        user_id=current_user.id,
        name=name,
        species=species,
        description=description,
        image=image
    )
    return plant

@router.get(
    "/plants",
    response_model=List[PlantResponse],
    description="Получить все растения пользователя"
)
def get_plants(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить все растения пользователя"""
    plants = Plant.get_user_plants(db, current_user.id)
    return plants

@router.get(
    "/plants/{plant_id}",
    response_model=PlantResponse,
    description="Получить растение по ID"
)
def get_plant(
    plant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить растение по ID"""
    plant = Plant.get_by_id(db, plant_id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Растение не найдено"
        )
    
    # Проверяем, принадлежит ли растение пользователю
    if plant.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому растению"
        )
    
    return plant

@router.patch(
    "/plants/{plant_id}",
    response_model=PlantResponse,
    description="Обновить растение"
)
def update_plant(
    plant_id: int,
    plant_data: PlantUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновить растение"""
    plant = Plant.get_by_id(db, plant_id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Растение не найдено"
        )
    
    # Проверяем, принадлежит ли растение пользователю
    if plant.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому растению"
        )
    
    # Обновляем растение
    updated_plant = plant.update(
        db=db,
        **plant_data.dict(exclude_unset=True)
    )
    
    return updated_plant

@router.put(
    "/plants/{plant_id}/image",
    response_model=PlantResponse,
    description="Обновить изображение растения"
)
async def update_plant_image(
    plant_id: int,
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновить изображение растения"""
    plant = Plant.get_by_id(db, plant_id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Растение не найдено"
        )
    
    # Проверяем, принадлежит ли растение пользователю
    if plant.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому растению"
        )
    
    # Обновляем изображение
    updated_plant = await Plant.save_image(db, plant_id, image)
    
    return updated_plant

@router.delete(
    "/plants/{plant_id}",
    description="Удалить растение"
)
def delete_plant(
    plant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удалить растение"""
    plant = Plant.get_by_id(db, plant_id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Растение не найдено"
        )
    
    # Проверяем, принадлежит ли растение пользователю
    if plant.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому растению"
        )
    
    # Удаляем растение
    result = plant.delete(db)
    
    return result 