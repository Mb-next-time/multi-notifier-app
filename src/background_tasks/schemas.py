from datetime import datetime

from pydantic import BaseModel

from notification_schedule.schemas import RepeatSettings


class NotificationAggregate(BaseModel):
    notification_schedule_id: int
    next_fire_at: datetime
    repeat_settings: RepeatSettings
    notification_id: int
    title: str
    body: str
    channel_id: int
    provider: str
    destination: str

class ResultOfSendNotification(BaseModel):
    code: str
    error: str | None
