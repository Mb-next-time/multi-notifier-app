from typing_extensions import Self

from pydantic import BaseModel, field_validator, model_validator
from pydantic.networks import validate_email

from channels.constants import (
    ChannelSchemeField, ChannelProvider, valid_providers,
)


class BaseChannel(BaseModel):
    provider: str
    destination: str

    @field_validator(ChannelSchemeField.PROVIDER.value)
    @classmethod
    def validate_provider(cls, value: str) -> str:
        if value and value.strip().lower() not in valid_providers:
            allowed_values: str = ", ".join(valid_providers)
            raise ValueError(f"'{value}' should be one of [{allowed_values}]")
        return value

    @model_validator(mode='after')
    def check_destination(self) -> Self:
        if self.provider == ChannelProvider.EMAIL.value:
            # Validation email format
            # Pydantic raises exception if the email isn't valid
            validate_email(self.destination)
        return self

class BodyChannel(BaseChannel):
    ...

class ResponseChannel(BaseChannel):
    id: int
    is_verified: bool

