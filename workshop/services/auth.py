from datetime import datetime
from enum import Enum
import hashlib
from http import HTTPStatus
import secrets
from typing import NewType, Optional
from uuid import uuid1

from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)
import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from workshop.config import settings
from workshop.db import get_session
from workshop.db.models import User
from workshop.schemas import (
    JsonWebTokens,
    UserCredentials,
    RefreshToken
)


class TokenType(str, Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'


UserId = NewType('UserId', int)


class AuthService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    @classmethod
    def hash_password(cls, password: str) -> str:
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    @classmethod
    def verify_password(cls, password: str, password_hash: str) -> bool:
        return secrets.compare_digest(cls.hash_password(password), password_hash)

    @classmethod
    def create_access_token(cls, user: User) -> str:
        current_time = datetime.utcnow()
        payload = {
            'user_id': user.id,
            'iat': current_time,
            'exp': current_time + settings.auth.access_token_expires_in,
            'type': TokenType.ACCESS
        }
        return jwt.encode(payload, settings.auth.jwt_secret, 'HS256')

    @classmethod
    def create_refresh_token(cls, user: User) -> str:
        current_time = datetime.utcnow()
        payload = {
            'user_id': user.id,
            'iat': current_time,
            'exp': current_time + settings.auth.refresh_token_expires_in,
            'type': TokenType.REFRESH
        }
        return jwt.encode(payload, settings.auth.jwt_secret, 'HS256')

    @classmethod
    def validate_access_token(cls, access_token: str) -> UserId:
        try:
            token_payload = jwt.decode(
                access_token,
                settings.auth.jwt_secret,
                ['HS256']
            )
        except jwt.PyJWTError:
            raise HTTPException(HTTPStatus.UNAUTHORIZED)

        if token_payload.get('type') != TokenType.ACCESS:
            raise HTTPException(HTTPStatus.UNAUTHORIZED)

        try:
            return token_payload['user_id']
        except KeyError:
            raise HTTPException(HTTPStatus.UNAUTHORIZED)

    @classmethod
    def validate_refresh_token(cls, refresh_token: str) -> UserId:
        try:
            token_payload = jwt.decode(
                refresh_token,
                settings.auth.jwt_secret,
                ['HS256']
            )
        except jwt.PyJWTError:
            raise HTTPException(HTTPStatus.UNAUTHORIZED)

        if token_payload.get('type') != TokenType.REFRESH:
            raise HTTPException(HTTPStatus.UNAUTHORIZED)

        try:
            return token_payload['user_id']
        except KeyError:
            raise HTTPException(HTTPStatus.UNAUTHORIZED)

    @classmethod
    def create_json_web_tokens(cls, user: User) -> JsonWebTokens:
        return JsonWebTokens(
            access_token=cls.create_access_token(user),
            refresh_token=cls.create_refresh_token(user)
        )

    def register_user(self, credentials: UserCredentials) -> JsonWebTokens:
        with self.session.begin():
            username = str(uuid1())
            password_hash = self.hash_password(
                credentials.password.get_secret_value()
            )
            user = User(
                email=credentials.email,
                username=username,
                password_hash=password_hash
            )
            self.session.add(user)

            try:
                self.session.flush()
            except IntegrityError:
                raise HTTPException(HTTPStatus.BAD_REQUEST,
                                    'Invalid credentials')

            return self.create_json_web_tokens(user)

    def authenticate_user(self, credentials: UserCredentials) -> JsonWebTokens:
        q = self.session.query(User).filter_by(email=credentials.email)
        user: Optional[User] = q.scalar()
        if (
            not user
            or not self.verify_password(
                credentials.password.get_secret_value(),
                user.password_hash
            )
        ):
            raise HTTPException(HTTPStatus.BAD_REQUEST, 'Invalid credentials')
        return self.create_json_web_tokens(user)

    def refresh_tokens(self, payload: RefreshToken) -> JsonWebTokens:
        user_id = self.validate_refresh_token(payload.refresh_token)
        user = self.session.query(User).get(user_id)
        if not user:
            raise HTTPException(HTTPStatus.UNAUTHORIZED)
        return self.create_json_web_tokens(user)


security = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserId:
    return AuthService.validate_access_token(credentials.credentials)
