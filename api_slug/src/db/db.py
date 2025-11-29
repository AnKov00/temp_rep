from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import (
    async_sessionmaker, 
    create_async_engine,
    AsyncSession, 
    AsyncEngine
)
from sqlalchemy.exc import SQLAlchemyError
from core.config import app_settings
from typing import AsyncGenerator, Annotated


class InternalError(Exception):
    pass


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
        try:
            yield session
            # Если не было исключений - коммитим транзакцию
            await session.commit()
        except SQLAlchemyError as e:
            # В случае ошибки откатываем транзакцию
            await session.rollback()
            raise HTTPException(
                status_code=500, 
                detail=f"Database error: {str(e)}"
            )
        finally:
            # Всегда закрываем сессию
            await session.close()


# Создание зависимости для работы с базой данных
db_dependency = Annotated[AsyncSession, Depends(get_async_session)]