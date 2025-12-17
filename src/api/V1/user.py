import httpx
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from schemas.user import UserRegisterSchema, UserLoginSchema
from db.db import db_dependency
from auth.auth import reg_user, authenticate_user, create_access_token


user_router = APIRouter(prefix="/user", tags=['user'])
auth_router = APIRouter(prefix="/auth", tags=['auth'])

@user_router.get("/{user_id}")
async def get_user(user_id: int):
    async with httpx.AsyncClient (base_url='https://jsonplaceholder.typicode.com') as client:
        response = await client.get(f'/user/{user_id}')
        return response.json()

@auth_router.post("/register")
async def register_user(user_data: UserRegisterSchema, db: db_dependency):
    try:
        return await reg_user(user_data=user_data, db=db)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"An error has occurred: {ex}")

@auth_router.post("/login")
async def login_for_access_token(login_data: UserLoginSchema, db: db_dependency):
    user = await authenticate_user(login_data, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"},)
    access_token = create_access_token(data={"sub": {"email": user.email}})
    return {"access_token": access_token, "token_type": "bearer"}