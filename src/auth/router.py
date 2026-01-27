from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.exc import IntegrityError
from starlette import status

from auth.exceptions import AuthIsFailed
from auth.schemas import UserIn, UserOut, Token
from auth.services import AuthService
from auth.constants import AuthLiterals
from auth.dependencies import get_auth_service
from src.constants import HttpClientCommonErrors

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
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists, please use a other",
        )
    except Exception as e:
        # to do logging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=HttpClientCommonErrors.SOMETHING_WENT_WRONG.value
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
    except AuthIsFailed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    except Exception as e:
        # to do logging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=HttpClientCommonErrors.SOMETHING_WENT_WRONG.value
        )
    return token
