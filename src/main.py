from fastapi import FastAPI

from notifications.router import notification_router

app = FastAPI()

app.include_router(notification_router)
