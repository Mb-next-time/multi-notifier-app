import logging

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from notifications.exceptions import NotificationNotFound
from notifications.router import notification_router
from auth.router import auth_router
from constants import HttpClientCommonErrorsLiteral
from notifications import handlers

app = FastAPI()

app.include_router(notification_router)
app.include_router(auth_router)

app.add_exception_handler(NotificationNotFound, handlers.notification_not_found_exception_handler)

@app.exception_handler(Exception)
async def common_exception_handler(request: Request, exc: Exception):
    logging.exception("The unexpected exception")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": HttpClientCommonErrorsLiteral.SOMETHING_WENT_WRONG}),
    )
