from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvConfig(BaseSettings):

    AI_API_KEY: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRES: int
    REFRESH_TOKEN_EXPIRES: int
    DATABASE_URI: str
 



    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
