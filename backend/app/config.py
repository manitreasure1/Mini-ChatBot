from datetime import timedelta
from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "your_email@gmail.com"
    MAIL_PASSWORD = "your_email_password"
    MAIL_DEFAULT_SENDER = "your_email@gmail.com"
    REDIS_URL: str
    NEBUIS_API_KEY:str
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=30)
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool
    CACHE_TYPE: str = "RedisCache"
    CACHE_REDIS_URL: str | None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.CACHE_REDIS_URL is None:
            self.CACHE_REDIS_URL = self.REDIS_URL


    SWAGGER: dict[str, Any] = {
        "title": "Flask Chat API"
        }
    SQLALCHEMY_ENGINE_OPTIONS:dict[str, bool|int] = {
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20
    }

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )





class TestConfig(BaseSettings):
    TESTING: bool =True
    SQLALCHEMY_DATABASE_URI: str 



