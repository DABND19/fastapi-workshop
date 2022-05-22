from http import HTTPStatus

from fastapi import APIRouter, Depends

from workshop.services import AuthService
from workshop.schemas import UserCredentials, JsonWebTokens, RefreshToken


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/sign-up', response_model=JsonWebTokens, status_code=HTTPStatus.CREATED)
def sign_up(payload: UserCredentials, service: AuthService = Depends()):
    return service.register_user(payload)


@router.post('/sign-in', response_model=JsonWebTokens)
def sign_in(payload: UserCredentials, service: AuthService = Depends()):
    return service.authenticate_user(payload)


@router.post('/refresh-tokens', response_model=JsonWebTokens)
def refresh_tokens(payload: RefreshToken, service: AuthService = Depends()):
    return service.refresh_tokens(payload)
