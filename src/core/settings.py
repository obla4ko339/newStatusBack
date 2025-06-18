from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    
    model_config = ConfigDict(env_file=".env", extra="ignore")

# class JWTSettings(EnvSettings):
#     """
#     Настройки для jwt
#     """

#     SECRET_KEY: str
#     ALGORITHM: str
#     ACCESS_TOKEN_EXPIRE: int


class DBSettings(EnvSettings):
    """
    Настройки для БД
    """

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str

    @property
    def connection_string(self):
        return f"postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:5432/{self.POSTGRES_DB}"


class Settings(EnvSettings):
    """
    Все настройки
    """

    project_name: str = "Тестовое задание: Чат"
    # api_str: str = "/api/v1"
    # DATABASE_URL: str = "postgresql+asyncpg://user:pass@db:5432/db"
    db: DBSettings = DBSettings()
    # jwt: JWTSettings = JWTSettings()
    # email: EmailSettings = EmailSettings()


settings = Settings()
