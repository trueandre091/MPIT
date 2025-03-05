from fastapi import APIRouter, HTTPException, Depends, status, Form
from database import get_db
from sqlalchemy.orm import Session
from datetime import datetime
from settings import get_settings

from services.auth_service import AuthService
from services.note_service import NoteCreate

from models.user import User
from models.note import Note

settings = get_settings()
router = APIRouter()
auth_service = AuthService()

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_note(
    title: str = Form(...),
    text: str = Form(...),
    plant_id: int = Form(None),
    day: datetime = Form(None),
    user: User = Depends(auth_service.verify_user),
    db: Session = Depends(get_db)
):
    if not any([plant_id, day]):
        raise HTTPException(status_code=400, detail="plant_id OR day is required")
    note = NoteCreate(title=title, text=text, user_id=user.id, plant_id=plant_id, day=day)
    note = Note.create(db, note.title, note.text, note.user_id, note.plant_id, note.day)
    return {
        "note": note.to_dict()
    }

@router.get("/get", status_code=status.HTTP_200_OK)
async def get_notes(
    user: User = Depends(auth_service.verify_user),
    db: Session = Depends(get_db)
):
    notes = Note.get_all(db, user.id)
    return {
        "notes": [note.to_dict() for note in notes]
    }

@router.get("/get/{note_id}", status_code=status.HTTP_200_OK)
async def get_note(
    note_id: int,
    user: User = Depends(auth_service.verify_user),
    db: Session = Depends(get_db)
):
    note = Note.get_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {
        "note": note.to_dict()
    }

@router.patch("/update/{note_id}", status_code=status.HTTP_200_OK)
async def update_note(
    note_id: int,
    title: str = Form(None),
    text: str = Form(None),
    plant_id: int = Form(None),
    day: datetime = Form(None),
    user: User = Depends(auth_service.verify_user),
    db: Session = Depends(get_db)
):
    if not any([title, text, plant_id, day]):
        raise HTTPException(status_code=400, detail="No fields to update")
    note = Note.get_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to update this note")
    note = NoteCreate(
        title=title if title else note.title,
        text=text if text else note.text,
        user_id=user.id,
        plant_id=plant_id if plant_id else note.plant_id,
        day=day if day else note.day
    )
    note = Note.update(db, note_id, **note.__dict__)
    return {
        "note": note.to_dict()
    }

@router.delete("/delete/{note_id}", status_code=status.HTTP_200_OK)
async def delete_note(
    note_id: int,
    user: User = Depends(auth_service.verify_user),
    db: Session = Depends(get_db)
):
    note = Note.get_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this note")
    Note.delete(db, note_id)
    return {
        "note": note.to_dict(),
        "detail": "Note deleted"
    }

