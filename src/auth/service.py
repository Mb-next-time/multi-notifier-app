from sqlalchemy import select
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from .exceptions import AuthIsFailed
from .schemas import UserIn
from . import models


class UserService:

    def __init__(self, database: Session):
        self.database = database
        self.password_hash = PasswordHash.recommended()

    def create(self, user_in: UserIn) -> models.User:
        user_in.password = self.password_hash.hash(user_in.password)
        user = models.User(**user_in.model_dump())
        self.database.add(user)
        self.database.flush()
        return user

    def get(self, user_in: UserIn) -> models.User:
        user = self.database.execute(select(models.User).filter_by(username=user_in.username)).scalar_one_or_none()
        if not user:
            raise AuthIsFailed
        if not self.password_hash.verify(user_in.password, user.password):
            raise AuthIsFailed
        return user


