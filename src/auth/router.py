import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status

from auth.exceptions import AuthIsFailed, AuthDuplication
from auth.schemas import UserIn, UserOut, Token
from auth.services import AuthService
from auth.constants import AuthLiterals
from auth.dependencies import get_auth_service


auth_router = APIRouter(prefix=f"/{AuthLiterals.URL.value}", tags=[AuthLiterals.TAGS])

@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
)
async def register(
    user_in: UserIn,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        created_user = auth_service.register_user(user_in)
    except AuthDuplication as error:
        logging.exception(error)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unfortunately, a user with this username already exists. Please choose another username.",
        )
    return created_user


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=Token,
)
async def login(
    user_in: UserIn,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Token:
    try:
        token = auth_service.login_user(user_in)
    except AuthIsFailed as error:
        logging.exception(error)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return token
