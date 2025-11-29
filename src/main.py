import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, EmailStr
from typing import Optional

from src.api import api_router
from core.config import uvicorn_options

class MyGetFuncResponseSchema(BaseModel):
    app_name: str
    number_of_months: int
    pi: float

class User(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None


app = FastAPI(
    docs_url="/api/openapi"
)
router = APIRouter()

@router.get("/path",responses={
                200: {"model": MyGetFuncResponseSchema},
                404: {"description": "Response not found"},
                400: {"description": "Invalid request"},
            })
def my_get_func():
    return {
        "app_name": "MyAPP",
        "number_of_months": 12,
        "pi": 3.14
    }

@router.post("/path", response_model=User)
def my_post_func(user: User):
    return user

@router.put("/path")
def my_put_func():
    pass

@router.delete("/path")
def my_delete_func():
    pass

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(router)
app.include_router(api_router)

if __name__ == "__main__":
    print(uvicorn_options)
    uvicorn.run("main:app", **uvicorn_options)