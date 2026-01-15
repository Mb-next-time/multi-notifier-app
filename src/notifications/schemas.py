from datetime import timedelta

from pydantic import BaseModel


class BaseNotification(BaseModel):
    title: str | None = None
    body: str | None = None
    interval: int

class BodyNotification(BaseNotification):
    ...

class Notification(BaseNotification):
    id: int



