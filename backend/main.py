from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from settings import get_settings
from database import create_db
from contextlib import asynccontextmanager
import os

from routers import auth, plants, notes

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not settings.DB_CREATED:
        create_db()
        settings.DB_CREATED = True

    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    yield

app = FastAPI(
    title="Easy API",
    description="API для Easy App",
    lifespan=lifespan
)

# routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(plants.router, prefix="/api/plants", tags=["plants"])
app.include_router(notes.router, prefix="/api/notes", tags=["notes"])


@app.get("/")
async def root():
    return {"detail": "Hello World"}












