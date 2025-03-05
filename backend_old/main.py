from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import auth, users, sessions, ai, plants, notes
from services.ai_service import ai_service
from config.settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="API для веб и мобильных приложений",
    version=settings.APP_VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL
)

# Добавляем описание безопасности для Swagger UI
app.swagger_ui_init_oauth = {
    "usePkceWithAuthorizationCodeGrant": True,
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Описание схемы безопасности
app.openapi_components = {
    "securitySchemes": {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
}

# Глобальные настройки безопасности
app.openapi_security = [{"bearerAuth": []}]

# Подключаем роутеры
app.include_router(auth.router, prefix=settings.API_PREFIX, tags=["Auth"])
app.include_router(users.router, prefix=settings.API_PREFIX, tags=["Users"])
app.include_router(sessions.router, prefix=settings.API_PREFIX, tags=["Sessions"])
app.include_router(ai.router, prefix=settings.API_PREFIX, tags=["AI"])
app.include_router(plants.router, prefix=settings.API_PREFIX, tags=["Plants"])
app.include_router(notes.router, prefix=settings.API_PREFIX, tags=["Notes"])

@app.on_event("startup")
async def startup_event():
    """Выполняется при запуске приложения"""
    # Загружаем модель
    if not ai_service.load_model():
        print("ПРЕДУПРЕЖДЕНИЕ: Не удалось загрузить модель!")

@app.get("/")
async def root():
    """
    Корневой эндпоинт с информацией о состоянии API
    """
    response = {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "online"
    }
    
    # Добавляем ссылки на документацию только в режиме разработки
    if settings.DEBUG:
        response.update({
            "docs": f"{settings.API_PREFIX}/docs",
            "redoc": f"{settings.API_PREFIX}/redoc",
            "openapi": f"{settings.API_PREFIX}/openapi.json"
        })
    
    return response

@app.middleware("http")
async def add_environment_header(request: Request, call_next):
    """Добавляем информацию об окружении в заголовки ответа"""
    response = await call_next(request)
    response.headers["X-Environment"] = settings.ENVIRONMENT
    return response 