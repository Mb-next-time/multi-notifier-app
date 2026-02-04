from typing import Annotated

from fastapi import APIRouter, Path, status
from fastapi.params import Depends, Query

from notifications.constants import NotificationLiteral
from notifications.schemas import BodyNotification, UpdateNotification, ResponseNotification, FilterNotification
from notifications.service import NotificationService
from notifications.dependencies import get_notification_service


notification_router = APIRouter(prefix=f"/{NotificationLiteral.URL.value}", tags=[NotificationLiteral.TAGS])

@notification_router.get(
    path="/",
    response_model=list[ResponseNotification]
)
async def list_notifications(
    notification_service: Annotated[NotificationService,Depends(get_notification_service)],
    filter_notification: Annotated[FilterNotification, Query()],
):
    return notification_service.get_list(filter_notification)

@notification_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseNotification
)
async def create_notification(
    notification: BodyNotification,
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
):
    created_notification = notification_service.create(notification)
    return created_notification

@notification_router.get(
    path=f"/{{{NotificationLiteral.NOTIFICATION_ID.value}}}",
    response_model=ResponseNotification
)
async def get_notification(
    notification_id: Annotated[int, Path(gt=0)],
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
):
    notification = notification_service.get(notification_id)
    return notification

@notification_router.put(
    path=f"/{{{NotificationLiteral.NOTIFICATION_ID.value}}}",
    response_model=ResponseNotification
)
async def update_notification(
    notification_id: Annotated[int, Path(gt=0)],
    notification: UpdateNotification,
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
):
    updated_notification = notification_service.update(notification_id, notification)
    return updated_notification

@notification_router.delete(
    path=f"/{{{NotificationLiteral.NOTIFICATION_ID.value}}}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_notification(
    notification_id: Annotated[int, Path(gt=0)],
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
):
    notification_service.delete(notification_id)
