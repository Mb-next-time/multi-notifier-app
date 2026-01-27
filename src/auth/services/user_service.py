from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.schemas import UserIn
from auth import models


class UserService:

    def __init__(self, database_session: Session) -> None:
        self.database_session = database_session

    def get(self, user_id: int) -> models.User:
        statement = select(models.User).where(
            models.User.id == user_id,
            models.User.is_deleted == False
        )
        user = self.database_session.execute(statement).scalar_one_or_none()
        return user

    def get_by_username(self, username: str) -> models.User:
        statement = select(models.User).where(
            models.User.is_deleted == False,
            models.User.username == username
        )
        user = self.database_session.execute(statement).scalar_one_or_none()
        return user


    def create_user(self, user_in: UserIn) -> models.User:
        user = models.User(**user_in.model_dump())
        self.database_session.add(user)
        self.database_session.flush()
        return user