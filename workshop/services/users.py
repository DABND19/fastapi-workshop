from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, defer

from workshop.db import get_session
from workshop.db.models import User
from workshop.schemas import UserUpdateSchema


class UsersService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def get_user_with_id(self, user_id: int) -> User:
        user = self.session.query(User).get(user_id)
        if not user:
            raise HTTPException(HTTPStatus.NOT_FOUND)
        return user

    def get_user_with_username(
        self,
        username: str
    ) -> User:
        q = self.session.query(User).filter_by(username=username)
        user = q.scalar()
        if not user:
            raise HTTPException(HTTPStatus.NOT_FOUND)
        return user

    def _update_user_email(self, user: User, email: str) -> None:
        with self.session.begin_nested():
            user.email = email
            self.session.add(user)
            try:
                self.session.flush()
            except IntegrityError:
                raise HTTPException(HTTPStatus.BAD_REQUEST,
                                    'Email is already in use')

    def _update_user_username(self, user: User, username: str) -> None:
        with self.session.begin_nested():
            user.username = username
            self.session.add(user)
            try:
                self.session.flush()
            except IntegrityError:
                raise HTTPException(HTTPStatus.BAD_REQUEST,
                                    'Username is already in use')

    def update_user(self, user_id: int, payload: UserUpdateSchema) -> User:
        with self.session.begin():
            user = self.get_user_with_id(user_id)

            patch_payload = payload.dict(exclude_unset=True,
                                         exclude={'username', 'email'})
            for field, value in patch_payload.items():
                setattr(user, field, value)
            self.session.add(user)
            self.session.flush()

            if payload.email is not None:
                self._update_user_email(user, payload.email)

            if payload.username is not None:
                self._update_user_username(user, payload.username)

            return user
