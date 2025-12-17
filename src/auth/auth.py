from datetime import timedelta, datetime, timezone
from typing import Optional, Annotated, Dict, List

import bcrypt
from asyncpg import UniqueViolationError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from starlette import status

from core.config import app_settings
from db.db import db_dependency
from models import User
from schemas.user import UserRegisterSchema, UserLoginSchema


#Секретная фраза для генерации и валидации токенов
JWT_SECRET = app_settings.jwt_secret
#Алгоритм хеширования
ALGORITHM = app_settings.algorithm
#Контекст для валидации и хеширования
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

#Генерация соли
def generate_salt():
    return bcrypt.gensalt().decode("utf-8")
#Хеширование пароля с использованием соли
def hash_password(password: str, salt: str):
    return bcrypt_context.hash(password + salt)

#Создание нового токена
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    #Копируем исходные данные, чтобы случайно их не испортить
    to_encode = data.copy()
    #Устанавливаем временной промежуток жизни токена
    expire = int((datetime.now(timezone.utc) + expires_delta).timestamp())
    #Добавляем время смерти токена
    to_encode.update({"exp": expire})
    #Генерируем токен из данных, секрета и алгоритма
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

#регистрация пользователя
async def reg_user(user_data: UserRegisterSchema, db: db_dependency):
    user_salt: str = generate_salt()
    try:
        create_user_statement: User = User(**user_data.model_dump(exclude={'password'}), #распаковываем данные пользователя, исключая пароль
                                           salt=user_salt, #Тут добавляем сгенерированную соль
                                           hash_password=hash_password(user_data.password, user_salt))
        #Добавляем пользователя в БД
        db.add(create_user_statement)
        await db.commit()
        return {"response": "User created successfully"}
    except UniqueViolationError:
        #Если возникает ошибка UniqueViolationError значит пользователь с такими данными уже есть
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Пользователь с такими данными уже есть')
    except Exception as ex:
        raise ex #Не понимаю эту конструкцию.

#Аутенитфикация пользователя
async def authenticate_user(login_data: UserLoginSchema, db: db_dependency):
    #Делаем SELECT-запрос в базу данных для нахождения пользователя по email
    result = await db.execute(select(User).where(User.email == login_data.email))
    user: Optional[User] = result.scalars().first()
    #пользователь будет авторизован, если он зарегистрирован и ввёл корректный пароль
    if not user:
        return False
    
    if not bcrypt_context.verify(login_data.password + user.salt, user.hash_password):
        return False
    return user 
    
