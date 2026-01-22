from fastapi import FastAPI

import notifications

app = FastAPI()

app.include_router(notifications.routers.notification_router)
