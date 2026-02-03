from enum import Enum

from fastapi import HTTPException
from starlette import status


class NotificationLiteral(Enum):
    HOW_OFTEN = "how_often"
    STEP = "step"
    TAGS = "notifications"
    NOTIFICATION_ID = "notification_id"
    NOTIFICATION_NOT_FOUND = "Notification not found"
    SOMETHING_WENT_WRONG = "Something went wrong, please try again later"
    URL = "notifications"


class NotificationSchemeFields(Enum):
    TITLE = "title"
    BODY = "body"
    REPEAT_INTERVAL = "repeat_interval"
    STARTUP_AT = "startup_at"

DEFAULT_NUMBER_PAGE = 1
DEFAULT_PAGE_LIMIT = 15

class RepeatInterval(Enum):
    ONCE = "once"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


VALID_REPEAT_INTERVALS = {
    repeat_interval.value for repeat_interval in RepeatInterval
}

EXCEPTION_NOTIFICATION_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=NotificationLiteral.NOTIFICATION_NOT_FOUND.value
)
