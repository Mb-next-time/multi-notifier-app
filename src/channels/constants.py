from enum import Enum


class ChannelLiteral(Enum):
    TAGS = "channels"
    CHANNEL_ID = "channel_id"
    URL = "channels"

class ChannelSchemeField(Enum):
    PROVIDER = "provider"
    DESTINATION = "destination"

class ChannelProvider(Enum):
    EMAIL = "email"

valid_providers = {
    channel_provider.value for channel_provider in ChannelProvider
}

DEFAULT_NUMBER_PAGE = 1
DEFAULT_PAGE_LIMIT = 15
