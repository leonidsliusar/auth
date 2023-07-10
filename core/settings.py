from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_LOGIN: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    DB: Optional[str] = None

    EMAIL_HOST: str
    EMAIL_PORT: str
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str

    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    ALGORITHM: str
    SECRET_KEY: str

    def __init__(self):
        super().__init__()
        self.set_db()

    def set_db(self):
        self.DB = f'postgresql+asyncpg://{self.DB_LOGIN}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


settings = Settings()
