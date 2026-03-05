from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator

from notification_schedule.constants import VALID_REPEAT_INTERVALS, NotificationScheduleLiteral


class RepeatSettings(BaseModel):
    how_often: str
    step: int = Field(ge=0)

    @field_validator(NotificationScheduleLiteral.HOW_OFTEN.value)
    @classmethod
    def how_often_validator(cls, value: str) -> str:
        if value.strip().lower() not in VALID_REPEAT_INTERVALS:
            allowed_values: str = ", ".join(VALID_REPEAT_INTERVALS)
            raise ValueError(f"'{value}' should be one of [{allowed_values}]")
        return value

class NotificationSchedule(BaseModel):
    name: str
    channel_id: int
    notification_id: int
    repeat_settings: RepeatSettings
    fire_at: datetime

    @field_validator(NotificationScheduleLiteral.FIRE_AT.value)
    @classmethod
    def startup_at_validator(cls, value: datetime) -> datetime:
        if not value.tzinfo or value.utcoffset() is None:
            raise ValueError(f"{NotificationScheduleLiteral.FIRE_AT.value} must include timezone offset (e.g. Z or +hh:mm/-hh:mm)")
        value = value.astimezone(timezone.utc)
        if value < datetime.now(timezone.utc):
            raise ValueError(f"{NotificationScheduleLiteral.FIRE_AT.value} must be set in future")
        return value.astimezone(timezone.utc)

class BodyNotificationSchedule(NotificationSchedule):
    pass

class ResponseNotificationSchedule(NotificationSchedule):
    id: int
