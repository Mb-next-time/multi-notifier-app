from fastapi import FastAPI

from notifications.router import notification_router
from auth.router import auth_router

app = FastAPI()

app.include_router(notification_router)
app.include_router(auth_router)
