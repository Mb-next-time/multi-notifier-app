from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator

from notifications import constants
from notifications.constants import DEFAULT_NUMBER_PAGE, DEFAULT_PAGE_LIMIT


class RepeatInterval(BaseModel):
    how_often: str
    step: int = Field(ge=0)

    @field_validator(constants.NotificationLiteral.HOW_OFTEN.value)
    @classmethod
    def how_often_validator(cls, value: str) -> str:
        if value.strip().lower() not in constants.VALID_REPEAT_INTERVALS:
            allowed_values: str = ", ".join(constants.VALID_REPEAT_INTERVALS)
            raise ValueError(f"'{value}' should be one of [{allowed_values}]")
        return value

class BaseNotification(BaseModel):
    title: str | None = None
    body: str | None = None
    repeat_interval: RepeatInterval
    startup_at: datetime

    @field_validator(constants.NotificationSchemeFields.STARTUP_AT.value)
    @classmethod
    def startup_at_validator(cls, value: datetime) -> datetime:
        if not value.tzinfo or value.utcoffset() is None:
            raise ValueError("startup_at must include timezone offset (e.g. Z or +hh:mm/-hh:mm)")
        value = value.astimezone(timezone.utc)
        if value < datetime.now(timezone.utc):
            raise ValueError("startup_at must be set in future")
        return value.astimezone(timezone.utc)

class BodyNotification(BaseNotification):
    ...

class UpdateNotification(BaseNotification):
    repeat_interval: RepeatInterval | None = None

class ResponseNotification(BaseNotification):
    id: int
    startup_at: datetime

    @field_validator(constants.NotificationSchemeFields.STARTUP_AT.value)
    @classmethod
    def startup_at_validator(cls, value: datetime) -> datetime:
        return value.astimezone(timezone.utc)

class FilterNotification(BaseModel):
    model_config = {"extra": "forbid"}

    page: int = Field(DEFAULT_NUMBER_PAGE, gt=0)
    limit: int = Field(DEFAULT_PAGE_LIMIT, gt=0, le=100)
