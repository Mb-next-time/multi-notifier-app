from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.exc import IntegrityError
from starlette import status

from auth.exceptions import AuthIsFailed
from auth.schemas import UserIn, UserOut, Token
from auth.service import UserService
from auth.constants import AuthLiterals
from auth.dependencies import get_user_service
from auth.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY
from src.constants import HttpClientCommonErrors

auth_router = APIRouter(prefix=f"/{AuthLiterals.URL.value}", tags=[AuthLiterals.TAGS])


# should move to other place
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


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
        created_user = user_service.register(user_in)
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
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> Token:
    try:
        user = user_service.authenticate_user(user_in)
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
    # move to service layer
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
