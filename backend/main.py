from fastapi import FastAPI, Request
from settings import get_settings
from database import create_db
from contextlib import asynccontextmanager

from routers import auth

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not settings.DB_CREATED:
        create_db()
        settings.DB_CREATED = True
    yield

app = FastAPI(
    title="Easy API",
    description="API для Easy App",
    lifespan=lifespan
)

# routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"detail": "Hello World"}












