from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
import jwt
from starlette import status

from auth import models
from auth.services import AuthService, UserService
from database import get_db
from auth.config import JWT_SECRET_KEY, JWT_ALGORITHM
from auth.schemas import TokenData


def get_user_service(database_session: Annotated[Session, Depends(get_db)]) -> UserService:
    return UserService(database_session)

def get_auth_service(user_service: Annotated[UserService, Depends(get_user_service)]) -> AuthService:
    return AuthService(user_service)

security = HTTPBearer()

def get_current_authenticated_user(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = authorization.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = user_service.get_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
