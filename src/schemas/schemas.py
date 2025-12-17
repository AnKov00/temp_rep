from pydantic import BaseModel, EmailStr
from typing import Optional


class MyGetFuncResponseSchema(BaseModel):
    app_name: str
    number_of_months: int
    pi: float

class User(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None