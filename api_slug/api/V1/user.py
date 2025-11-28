import httpx
from fastapi import APIRouter

user_router = APIRouter(prefix="/user", tags=['user'])

@user_router.get("/{user_id}")
async def get_user(user_id: int):
    async with httpx.AsyncClient (base_url='https://jsonlaceholder.typicode.com') as client:
        response = await client.get(f'/user/{user_id}')
        return response.json
