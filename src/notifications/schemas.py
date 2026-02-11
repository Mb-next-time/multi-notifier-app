from pydantic import BaseModel, Field, field_validator

from notifications.constants import DEFAULT_NUMBER_PAGE, DEFAULT_PAGE_LIMIT, NotificationSchemeField, valid_statuses


class BaseNotification(BaseModel):
    title: str
    body: str

class BodyNotification(BaseNotification):
    ...

class UpdateNotification(BaseNotification):
    title: str | None = None
    body: str | None = None
    status: str | None = None

    @field_validator(NotificationSchemeField.STATUS.value)
    @classmethod
    def status_validator(cls, value: str) -> str:
        if value and value.strip().lower() not in valid_statuses:
            allowed_values: str = ", ".join(valid_statuses)
            raise ValueError(f"'{value}' should be one of [{allowed_values}]")
        return value

class ResponseNotification(BaseNotification):
    id: int
    status: str

class FilterNotification(BaseModel):
    model_config = {"extra": "forbid"}

    page: int = Field(DEFAULT_NUMBER_PAGE, gt=0)
    limit: int = Field(DEFAULT_PAGE_LIMIT, gt=0, le=100)
