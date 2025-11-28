import multiprocessing
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    app_port: int = 8000
    app_host: str = 'localhost'
    reload: bool = True
    cpu_count: int | None = None

    class Config:
        _env_file = ".env"
        _extra = 'allow'

app_settings = AppSettings()

#Набор опций для запуска сервера
uvicorn_options = {
    "host": app_settings.app_host,
    "port": app_settings.app_port,
    "workers": app_settings.cpu_count or multiprocessing.cpu_count(),
    "reload": app_settings.reload
}