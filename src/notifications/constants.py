from enum import Enum


class NotificationLiteral(Enum):
    TAGS = "notifications"
    NOTIFICATION_ID = "notification_id"
    NOTIFICATION_NOT_FOUND = "Notification not found"
    URL = "notifications"

class NotificationSchemeField(Enum):
    BODY = "body"

DEFAULT_NUMBER_PAGE = 1
DEFAULT_PAGE_LIMIT = 15
