from enum import Enum


class NotificationScheduleLiteral(Enum):
    HOW_OFTEN = "how_often"
    STEP = "step"
    TAGS = "notification_schedules"
    URL = "notification_schedules"
    FIRE_AT = "fire_at"


class RepeatInterval(Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


VALID_REPEAT_INTERVALS = {
    repeat_interval.value for repeat_interval in RepeatInterval
}