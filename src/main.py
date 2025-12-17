import uvicorn
from fastapi import FastAPI, APIRouter, BackgroundTasks
from sqlalchemy import text

from db.db import db_dependency
from api import api_router
from core.config import uvicorn_options
from schemas.schemas import MyGetFuncResponseSchema, User
app = FastAPI(
    docs_url="/api/openapi"
)
router = APIRouter()

def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


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

@app.get('/ping')
async def ping(db: db_dependency):
    try:
        result = await db.execute(text("SELECT 1"))
        return result
    except Exception:
        return False

app.include_router(router)
app.include_router(api_router)

if __name__ == "__main__":
    print(uvicorn_options)
    uvicorn.run("main:app", **uvicorn_options)