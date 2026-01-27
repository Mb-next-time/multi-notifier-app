from datetime import timedelta

from auth.config import ACCESS_TOKEN_EXPIRE_MINUTES
from auth.exceptions import AuthIsFailed
from auth.schemas import UserIn, Token
from auth import models
from auth.utils import hash_password, verify_password, TokenUtils
from auth.services.user_service import UserService


class AuthService:

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def _authenticate_user(self, user_in: UserIn) -> models.User:
        user = self.user_service.get_by_username(user_in.username)
        if not (user and verify_password(user_in.password, user.password)):
            raise AuthIsFailed
        return user

    def register_user(self, user_in: UserIn) -> models.User:
        user_in.password = hash_password(user_in.password)
        user = self.user_service.create_user(user_in)
        return user

    def login_user(self, user_in: UserIn) -> Token:
        user = self._authenticate_user(user_in)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = TokenUtils.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")