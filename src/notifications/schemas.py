from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator

from notifications import constants

class RepeatInterval(BaseModel):
    how_often: str
    step: int = Field(ge=0)

    @field_validator(constants.NotificationLiteral.HOW_OFTEN.value)
    @classmethod
    def how_often_validator(cls, value: str) -> str:
        if value.strip().lower() not in constants.valid_repeat_intervals:
            allowed_values: str = ", ".join(constants.valid_repeat_intervals)
            raise ValueError(f"'{value}' should be one of [{allowed_values}]")
        return value

class BaseNotification(BaseModel):
    title: str | None = None
    body: str | None = None
    repeat_interval: RepeatInterval
    startup_at: datetime

    @field_validator(constants.NotificationLiteral.STARTUP_AT.value)
    @classmethod
    def startup_at_validator(cls, value: datetime) -> datetime:
        if not value.tzinfo or value.utcoffset() is None:
            raise ValueError("startup_at must include timezone offset (e.g. Z or +hh:mm/-hh:mm)")
        return value.astimezone(timezone.utc)

class BodyNotification(BaseNotification):
    ...

class UpdateNotification(BaseNotification):
    repeat_interval: RepeatInterval | None = None

class ResponseNotification(BaseNotification):
    id: int
