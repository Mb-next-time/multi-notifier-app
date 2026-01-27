from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from auth.services import AuthService, UserService
from database import get_db


def get_user_service(database_session: Annotated[Session, Depends(get_db)]) -> UserService:
    return UserService(database_session)

def get_auth_service(user_service: Annotated[UserService, Depends(get_user_service)]) -> AuthService:
    return AuthService(user_service)
