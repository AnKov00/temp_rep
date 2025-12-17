from sqlalchemy.ext.declarative import declarative_base

#базовая модель для создания других моделей и интеграции с alembic 
Base = declarative_base()