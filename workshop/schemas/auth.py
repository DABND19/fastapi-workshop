from pydantic import SecretStr

from .base import APISchema


class UserCredentials(APISchema):
    email: str
    password: SecretStr


class AccessToken(APISchema):
    access_token: str


class RefreshToken(APISchema):
    refresh_token: str


class JsonWebTokens(AccessToken, RefreshToken):
    pass
