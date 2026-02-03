from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=r'^[a-zA-Z0-9_\-.]+$')

class UserIn(UserBase):
    password: str = Field(min_length=8, max_length=64)

class UserOut(UserBase):
    ...