from fastapi import APIRouter, Depends

from workshop.services import strict_authorizer, UsersService
from workshop.schemas import (
    UserSchema,
    UserUpdateSchema,
    SelfUserSchema
)


router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/me', response_model=SelfUserSchema)
def get_self(
    service: UsersService = Depends(),
    user_id: int = Depends(strict_authorizer)
):
    return service.get_user_with_id(user_id)


@router.patch('/me', response_model=SelfUserSchema)
def update_self(
    payload: UserUpdateSchema,
    service: UsersService = Depends(),
    user_id: int = Depends(strict_authorizer)
):
    return service.update_user(user_id, payload)


@router.get('/{username}', response_model=UserSchema)
def get_user(username: str, service: UsersService = Depends()):
    return service.get_user_with_username(username)
