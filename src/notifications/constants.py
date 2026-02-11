from enum import Enum


class NotificationLiteral(Enum):
    TAGS = "notifications"
    NOTIFICATION_ID = "notification_id"
    NOTIFICATION_NOT_FOUND = "Notification not found"
    URL = "notifications"

class NotificationSchemeField(Enum):
    TITLE = "title"
    BODY = "body"
    STATUS = "status"

class NotificationStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"

valid_statuses = {
    notification_status.value for notification_status in NotificationStatus
}

DEFAULT_NUMBER_PAGE = 1
DEFAULT_PAGE_LIMIT = 15
