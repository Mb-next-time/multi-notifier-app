import logging

from fastapi import HTTPException
from starlette import status
from starlette.requests import Request

from notifications.constants import NotificationLiteral

async def notification_not_found_exception_handler(request: Request, exc: Exception):
    logging.exception(exc)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=NotificationLiteral.NOTIFICATION_NOT_FOUND.value
    )
