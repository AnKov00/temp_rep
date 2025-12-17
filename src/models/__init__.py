"""Добавляем две модели (базовую и первую) чтобы alembic мог их видеть 
и автоматически генерировать миграции
Инициировать alembic командой: alembic init -t async alembic
После чего нужно передать метадату базовой модели в target_metadata в директории alembic
alembic revision --autogenerate -m "Initial migration" - Создаст миграцию в автоматическом режиме
alembic upgrade head - применить миграцию
alembic downgrade -n ---- для отката миграции, где (n) - это количество миграций
"""
__all__ = [
    "Base",
    "ShortedUrl",
    "User"
]

from .base import Base
from .shorted_url import ShortedUrl
from .user_model import User