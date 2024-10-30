from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_server: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str
    insert_data_mode: bool

    class Config:
        env_file = ".env"


settings = Settings()