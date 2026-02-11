from fastapi import APIRouter
from app.api.health import router as health_router
from app.modules.users.api.routes import router as users_router
from app.modules.vocabulary.api.routes import router as vocabulary_router
from app.modules.exercises.api.routes import router as exercises_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(users_router)
api_router.include_router(vocabulary_router)
api_router.include_router(exercises_router)
