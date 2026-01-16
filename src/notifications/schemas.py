from pydantic import BaseModel, Field, field_validator

from notifications import constants

class RepeatInterval(BaseModel):
    how_often: str = constants.RepeatInterval.ONCE.value
    step: int = Field(default=0, ge=0)

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
    interval: RepeatInterval

class BodyNotification(BaseNotification):
    ...

class Notification(BaseNotification):
    id: int



