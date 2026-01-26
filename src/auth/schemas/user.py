from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str

class UserIn(UserBase):
    password: str = Field(min_length=8)

class UserOut(UserBase):
    ...