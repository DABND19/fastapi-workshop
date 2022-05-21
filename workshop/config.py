from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    db_url: str = 'sqlite:///./database.sqlite'


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
