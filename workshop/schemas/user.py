from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import APISchema


class UserBaseSchema(APISchema):
    username: str = Field(min_length=4, max_length=64,
                          regex=r'^[a-zA-Z0-9_.-]+$')


class UserUpdateSchema(UserBaseSchema):
    username: Optional[str] = Field(min_length=4, max_length=64,
                                     regex=r'^[a-zA-Z0-9_.-]+$')
    email: Optional[str]


class UserSchema(UserBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class SelfUserSchema(UserSchema):
    email: str
