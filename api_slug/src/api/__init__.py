from fastapi import APIRouter
from src.api.V1.user import user_router

api_router = APIRouter()

api_router.include_router(user_router)