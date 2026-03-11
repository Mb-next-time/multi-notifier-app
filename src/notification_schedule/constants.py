from enum import Enum


class NotificationScheduleLiteral(Enum):
    HOW_OFTEN = "how_often"
    STEP = "step"
    TAGS = "notification_schedules"
    URL = "notification_schedules"
    NEXT_FIRE_AT = "next_fire_at"
    NOTIFICATION_SCHEDULE_ID = "notification_schedule_id"
    REPEAT_SETTINGS = "repeat_settings"
    STATUS = "status"

class NotificationScheduleStatus(Enum):
    RUNNING = "running"
    DONE = "done"

class RepeatInterval(Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

VALID_REPEAT_INTERVALS = {
    repeat_interval.value for repeat_interval in RepeatInterval
}