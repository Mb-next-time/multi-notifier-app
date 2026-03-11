from enum import Enum


class NotificationDeliveryLiteral(Enum):
    CURRENT_ATTEMPT = "current_attempt"
    STATUS = "status"
    ERROR_MESSAGE = "error_message"
    DELIVERED_AT = "delivered_at"

class NotificationDeliveryStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"

NUMBER_OF_NOTIFICATIONS_TO_SEND = 5
MAX_DELIVERY_ATTEMPTS = 10
