from enum import Enum

class NotificationLiteral(Enum):
    HOW_OFTEN = "how_often"
    STEP = "step"
    TAGS = "notifications"
    NOTIFICATION_ID = "notification_id"
    NOTIFICATION_NOT_FOUND = "Notification not found"
    SOMETHING_WENT_WRONG = "Something went wrong, please try again later"
    URL = "notifications"
    STARTUP_AT = "startup_at"


class NotificationSchemeFields(Enum):
    TITLE = "title"
    BODY = "body"
    REPEAT_INTERVAL = "repeat_interval"

DEFAULT_NUMBER_PAGE = 1
DEFAULT_PAGE_LIMIT = 15

class RepeatInterval(Enum):
    ONCE = "once"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


valid_repeat_intervals = {
    repeat_interval.value for repeat_interval in RepeatInterval
}
