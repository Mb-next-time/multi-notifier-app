from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.exc import IntegrityError
from starlette import status

from .exceptions import AuthIsFailed
from .schemas import UserIn, UserOut
from .service import UserService
from .constants import AuthLiterals
from .dependencies import get_user_service
from src.constants import HttpClientCommonErrors

auth_router = APIRouter(prefix=f"/{AuthLiterals.URL.value}", tags=[AuthLiterals.TAGS])

@auth_router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
)
async def signup(
    user_in: UserIn,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        created_user = user_service.create(user_in)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists, please use a other",
        )
    except Exception as e:
        # to do logging
        print(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=HttpClientCommonErrors.SOMETHING_WENT_WRONG.value
        )
    return created_user


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=UserOut,
)
async def login(user_in: UserIn, user_service: Annotated[UserService, Depends(get_user_service)]):
    try:
        user = user_service.get(user_in)
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
    return user

