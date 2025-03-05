import os
from PIL import Image
from io import BytesIO
from settings import get_settings
from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import Optional

settings = get_settings()

def get_image_url(plant_id: int, filename: str) -> str:
    """Возвращает безопасный URL изображения для фронтенда"""
    if not filename:
        return ""
    return f"/api/plants/{plant_id}/image"

async def get_plant_image(file_path: str) -> FileResponse:
    """Возвращает изображение как FileResponse"""
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(
        file_path,
        media_type="image/jpeg",
        filename=os.path.basename(file_path)
    )

async def save_upload_image(file: UploadFile, plant_id: int) -> str:
    """
    Сохраняет загруженное изображение в файл
    Возвращает имя файла
    """  
    try:
        if not file.content_type.startswith('image/'):
            raise ValueError("Файл должен быть изображением")

        contents = await file.read()
        image = Image.open(BytesIO(contents))

        if image.mode != 'RGB':
            image = image.convert('RGB')

        max_size = (1200, 1200)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

        filename = f"{plant_id}_plant.jpg"
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        image.save(file_path, 'JPEG', quality=85, optimize=True)

        return filename
        
    except Exception as e:
        print(f"Error saving image: {e}")
        return ""
    finally:
        await file.seek(0)

def delete_plant_image(filename: str) -> bool:
    """Удаляет изображение растения"""
    if not filename:
        return True
        
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        return True
    except Exception as e:
        print(f"Error deleting image: {e}")
        return False

def get_image_path(filename: str) -> Optional[str]:
    """Возвращает полный путь к файлу изображения"""
    if not filename:
        return None
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    return file_path if os.path.exists(file_path) else None 