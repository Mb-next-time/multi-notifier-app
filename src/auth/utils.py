from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from auth.config import JWT_SECRET_KEY, JWT_ALGORITHM


class TokenUtils:

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            # default time to expire
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt


password_hash = PasswordHash.recommended()