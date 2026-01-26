from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from auth.service import UserService
from database import get_db

def get_user_service(database: Annotated[Session, Depends(get_db)]) -> UserService:
    return UserService(database)