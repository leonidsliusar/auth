from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_LOGIN: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    DB: Optional[str] = None

    def __init__(self):
        super().__init__()
        self.set_db()

    def set_db(self):
        self.DB = f'postgresql+asyncpg://{self.DB_LOGIN}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


settings = Settings()
