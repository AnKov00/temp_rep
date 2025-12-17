from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import (
    async_sessionmaker, 
    create_async_engine,
    AsyncSession, 
)
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import AsyncGenerator, Annotated

from core.config import app_settings


# Создание асинхронного движка SQLAlchemy
engine = create_async_engine(
    app_settings.postgres_dsn.unicode_string(),
    echo=True,  # Для отладки SQL запросов
    future=True
)

# Создание фабрики сессий
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для получения асинхронной сессии БД.
    Автоматически управляет жизненным циклом сессии.
    """
    async with async_session() as session:
        #использование контекстного менеджера для управления транзакцией
        async with session.begin():
            try:
                yield session
                # Если не было исключений коммит транзакции произойдёт автоматически
            except IntegrityError as e:
                # В случае ошибки транзакция откатывается автоматически
                
                raise HTTPException(
                    status_code=409, 
                    detail=f"Data integrity error: {str(e.orig)}"
                    )
            except SQLAlchemyError as e:
                raise HTTPException(
                    status_code=500, 
                    detail=f"Database error: {str(e)}"
                    )
            finally:
                # Всегда закрываем сессию
                await session.close()


# Создание зависимости для работы с базой данных
db_dependency = Annotated[AsyncSession, Depends(get_async_session)]