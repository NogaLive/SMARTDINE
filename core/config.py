# core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Si estas variables no existen en el entorno, la app no arranca.
    # Esto previene despliegues inseguros con configuraciones por defecto.
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    DB_CONNECTION_STRING: str

    class Config:
        env_file = ".env.prod"

settings = Settings()