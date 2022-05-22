from datetime import timedelta
from pydantic import BaseSettings


class AuthSettings(BaseSettings):
    jwt_secret: str = 'secret_key'
    access_token_expires_in: timedelta = timedelta(days=1)
    refresh_token_expires_in: timedelta = timedelta(weeks=2)


class Settings(BaseSettings):
    db_url: str = 'sqlite:///./database.sqlite'
    auth: AuthSettings = AuthSettings()


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
