from fastapi import APIRouter
from api.V1.user import user_router, auth_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(auth_router)