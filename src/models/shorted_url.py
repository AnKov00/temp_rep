from datetime import datetime, timezone

from sqlalchemy import String, Column, Integer, TIMESTAMP

from .base import Base

#Первая модель - таблица для хранения "slug"
class ShortedUrl(Base):
    __tablename__ = "url"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    origin = Column(String(256))
    shorted_url = Column(String(256), unique=True, index=True, nullable=False)
    create_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))