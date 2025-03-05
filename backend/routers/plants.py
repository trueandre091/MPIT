from fastapi import APIRouter, HTTPException, Depends, status, Form, File, UploadFile
from database import get_db
from sqlalchemy.orm import Session
from typing import Optional
from settings import get_settings
from fastapi.responses import JSONResponse, FileResponse
from services.image_service import save_upload_image, delete_plant_image, get_plant_image, get_image_path

from services.auth_service import AuthService
from services.plant_service import PlantCreate

from models.user import User
from models.plant import Plant

settings = get_settings()
router = APIRouter()
auth_service = AuthService()

@router.get("/{plant_id}/image")
async def get_plant_image_endpoint(
    plant_id: int,
    user: User = Depends(auth_service.verify_user),
    db: Session = Depends(get_db)
):
    plant = Plant.get_by_id(db, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    if plant.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to access this image")
    
    file_path = get_image_path(plant.image)
    if not file_path:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return await get_plant_image(file_path)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_plant(
    name: str = Form(...),  
    description: str = Form(None),
    image: UploadFile = File(None),
    user: User = Depends(auth_service.verify_user),
    db: Session = Depends(get_db)
):
    plant = PlantCreate(name=name, user_id=user.id, description=description)
    plant = Plant.create(db, plant.name, plant.user_id, plant.description)

    if image:
        image_path = await save_upload_image(image, plant.id)
        if image_path:
            plant = Plant.update(db, plant.id, image=image_path)
    
    return {
        "plant": plant.to_dict(True)
    }

@router.delete("/delete/{plant_id}", status_code=status.HTTP_200_OK)
async def delete_plant(
    plant_id: int,
    user: User = Depends(auth_service.verify_user),
    db: Session = Depends(get_db)
):
    plant = Plant.get_by_id(db, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    if plant.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this plant")
    Plant.delete(db, plant_id)
    delete_plant_image(plant.image)
    return {
        "plant": plant.to_dict(True),
        "detail": "Plant deleted"
    }

@router.get("/get", status_code=status.HTTP_200_OK)
async def get_plants(
    user: User = Depends(auth_service.verify_user),
    db: Session = Depends(get_db)
):
    plants = Plant.get_all_by_user_id(db, user.id)
    if not plants:
        raise HTTPException(status_code=404, detail="No plants found")
    response = []
    for plant in plants:
        response.append(plant.to_dict(True))
    return response

@router.get("/get/{plant_id}", status_code=status.HTTP_200_OK)
async def get_plant(
    plant_id: int,
    user: User = Depends(auth_service.verify_user),
    db: Session = Depends(get_db)
):
    plant = Plant.get_by_id(db, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return {
        "plant": plant.to_dict(True)
    }

@router.patch("/update/{plant_id}", status_code=status.HTTP_200_OK)
async def update_plant(
    plant_id: int,
    name: str = Form(...),
    description: str = Form(...),
    image: str = Form(...),
    user: User = Depends(auth_service.verify_user),
    db: Session = Depends(get_db)
):
    plant = Plant.get_by_id(db, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    if plant.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to update this plant")
    plant = PlantCreate(name=name, user_id=user.id, description=description, image=image)
    plant = Plant.update(db, plant_id, **plant.__dict__)
    return {
        "plant": plant.to_dict(True)
    }


