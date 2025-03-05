from fastapi import HTTPException
from datetime import datetime, UTC

from models.plant import Plant
from database import get_db

def validate_title(title: str):
    if len(title) < 2 or len(title) > 20:
        return False
    return True

def validate_text(text: str):
    if len(text) < 2 or len(text) > 1000:
        return False
    return True

def validate_plant_id(plant_id: int):
    db = next(get_db())
    if not Plant.get_by_id(db, plant_id):
        return False
    return True

def validate_day(day: datetime):
    if day.timestamp() < datetime.now(UTC).timestamp():
        return False
    return True

class NoteCreate:
    def __init__(self, title: str, text: str, user_id: int, plant_id: int = None, day: datetime = None):
        if not all(
            [
                validate_title(title) if title else True,
                validate_text(text) if text else True,
                validate_plant_id(plant_id) if plant_id else True,
                validate_day(day) if day else True,
            ]
        ):
            raise HTTPException(status_code=406, detail="Invalid title, text, user_id, plant_id, or day")
        self.title = title
        self.text = text
        self.user_id = user_id
        self.plant_id = plant_id
        self.day = day

