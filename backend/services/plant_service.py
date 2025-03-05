from datetime import datetime
from fastapi import HTTPException

def validate_name(name: str):
    if any(
        [
            len(name) < 2,
            len(name) > 50,
        ]
    ):
        return False
    return True

def validate_image(image: str):
    return True

class PlantCreate:
    def __init__(self, name: str, user_id: int, description: str = "", image: str = ""):
        if not all(
            [
                validate_name(name),
                validate_image(image),
            ]
        ):
            raise HTTPException(status_code=406, detail="Invalid name, user_id, description, or image")
        self.name = name
        self.user_id = user_id
        self.description = description
        self.image = image
