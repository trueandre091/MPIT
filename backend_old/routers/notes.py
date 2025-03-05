from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from database import get_db
from models.note import Note
from models.plant import Plant
from models.user import User
from schemas.notes import NoteCreate, NoteResponse, NoteUpdate
from routers.auth import get_current_user

router = APIRouter()

@router.post(
    "/notes",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    description="Создать новую заметку"
)
def create_note(
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать новую заметку"""
    # Если указан plant_id, проверяем, что растение принадлежит пользователю
    if note_data.plant_id:
        plant = Plant.get_by_id(db, note_data.plant_id)
        if not plant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Растение не найдено"
            )
        
        if plant.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет доступа к этому растению"
            )
    
    # Создаем заметку
    note = Note.create(
        db=db,
        title=note_data.title,
        content=note_data.content,
        plant_id=note_data.plant_id,
        day=note_data.day
    )
    
    return note

@router.get(
    "/notes/plant/{plant_id}",
    response_model=List[NoteResponse],
    description="Получить все заметки для растения"
)
def get_plant_notes(
    plant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить все заметки для растения"""
    # Проверяем, что растение принадлежит пользователю
    plant = Plant.get_by_id(db, plant_id)
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Растение не найдено"
        )
    
    if plant.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому растению"
        )
    
    # Получаем заметки
    notes = Note.get_plant_notes(db, plant_id)
    
    return notes

@router.get(
    "/notes/day/{day}",
    response_model=List[NoteResponse],
    description="Получить все заметки за день"
)
def get_day_notes(
    day: date,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить все заметки за день"""
    # Получаем заметки пользователя за день
    notes = Note.get_user_day_notes(db, current_user.id, day)
    
    return notes

@router.get(
    "/notes/{note_id}",
    response_model=NoteResponse,
    description="Получить заметку по ID"
)
def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить заметку по ID"""
    note = Note.get_by_id(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заметка не найдена"
        )
    
    # Проверяем, что заметка принадлежит растению пользователя
    if note.plant_id:
        plant = Plant.get_by_id(db, note.plant_id)
        if plant and plant.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет доступа к этой заметке"
            )
    
    return note

@router.put(
    "/notes/{note_id}",
    response_model=NoteResponse,
    description="Обновить заметку"
)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновить заметку"""
    note = Note.get_by_id(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заметка не найдена"
        )
    
    # Проверяем, что заметка принадлежит растению пользователя
    if note.plant_id:
        plant = Plant.get_by_id(db, note.plant_id)
        if plant and plant.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет доступа к этой заметке"
            )
    
    # Если в обновлении указан plant_id, проверяем, что растение принадлежит пользователю
    if note_data.plant_id and note_data.plant_id != note.plant_id:
        plant = Plant.get_by_id(db, note_data.plant_id)
        if not plant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Растение не найдено"
            )
        
        if plant.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет доступа к этому растению"
            )
    
    # Обновляем заметку
    updated_note = note.update(
        db=db,
        **note_data.dict(exclude_unset=True)
    )
    
    return updated_note

@router.delete(
    "/notes/{note_id}",
    description="Удалить заметку"
)
def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удалить заметку"""
    note = Note.get_by_id(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заметка не найдена"
        )
    
    # Проверяем, что заметка принадлежит растению пользователя
    if note.plant_id:
        plant = Plant.get_by_id(db, note.plant_id)
        if plant and plant.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет доступа к этой заметке"
            )
    
    # Удаляем заметку
    result = note.delete(db)
    
    return result 