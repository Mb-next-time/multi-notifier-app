import logging

from fastapi import FastAPI, APIRouter
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from notifications.exceptions import NotificationNotFound
from notifications.router import notification_router
from auth.router import auth_router
from constants import HttpClientCommonErrorsLiteral, API_URL_V1
from notifications import handlers

api_router = APIRouter(prefix=API_URL_V1)
api_router.include_router(notification_router)
api_router.include_router(auth_router)

app = FastAPI()
app.include_router(api_router)
app.add_exception_handler(NotificationNotFound, handlers.notification_not_found_exception_handler)

@app.exception_handler(Exception)
async def common_exception_handler(request: Request, exc: Exception):
    logging.exception("The unexpected exception")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": HttpClientCommonErrorsLiteral.SOMETHING_WENT_WRONG}),
    )
