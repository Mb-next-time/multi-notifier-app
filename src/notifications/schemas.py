from pydantic import BaseModel, Field

from notifications.constants import DEFAULT_NUMBER_PAGE, DEFAULT_PAGE_LIMIT


class BaseNotification(BaseModel):
    body: str

class BodyNotification(BaseNotification):
    ...

class UpdateNotification(BaseNotification):
    body: str | None = None

class ResponseNotification(BaseNotification):
    id: int

class FilterNotification(BaseModel):
    model_config = {"extra": "forbid"}

    page: int = Field(DEFAULT_NUMBER_PAGE, gt=0)
    limit: int = Field(DEFAULT_PAGE_LIMIT, gt=0, le=100)
