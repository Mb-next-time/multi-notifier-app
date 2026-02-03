from enum import Enum

from fastapi import HTTPException
from starlette import status


class HttpClientCommonErrorsLiteral(Enum):
    SOMETHING_WENT_WRONG = "Something went wrong, please try again later"


EXCEPTION_INTERNAL_ERROR = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail=HttpClientCommonErrorsLiteral.SOMETHING_WENT_WRONG.value
)
