from typing import Annotated

from fastapi import APIRouter, Path, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.exc import NoResultFound

from notifications import constants
from notifications.constants import NotificationLiteral
from notifications.schemas import Notification, BodyNotification, UpdateNotification
from notifications.service import NotificationService
from notifications.dependencies import get_notification_service


notification_router = APIRouter(prefix="/notifications")

@notification_router.get(
    path="/",
    tags=[NotificationLiteral.TAGS],
    response_model=list[Notification]
)
async def list_notifications(notification_service: Annotated[NotificationService, Depends(get_notification_service)]):
    try:
        notifications = notification_service.get_list()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=NotificationLiteral.SOMETHING_WENT_WRONG.value
        )
    return notifications


@notification_router.post(
    path="/",
    tags=[NotificationLiteral.TAGS],
    status_code=status.HTTP_201_CREATED,
    response_model=Notification
)
async def create_notification(
    notification: BodyNotification,
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
) -> Notification:
    try:
        created_notification = notification_service.create(notification)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=NotificationLiteral.SOMETHING_WENT_WRONG.value
        )
    return created_notification

@notification_router.get(
    path="/{notification_id}",
    tags=[constants.NotificationLiteral.TAGS],
    response_model=Notification
)
async def get_notification(
    notification_id: Annotated[int, Path(gt=0)],
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
):
    try:
        notification = notification_service.get_by_id(notification_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NotificationLiteral.NOTIFICATION_NOT_FOUND.value
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=NotificationLiteral.SOMETHING_WENT_WRONG.value
        )
    return notification


@notification_router.put(
    path="/{notification_id}",
    tags=[constants.NotificationLiteral.TAGS],
    response_model=Notification
)
async def update_notification(
    notification_id: Annotated[int, Path(gt=0)],
    notification: UpdateNotification,
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
):
    try:
        updated_notification = notification_service.update(notification_id, notification)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NotificationLiteral.NOTIFICATION_NOT_FOUND.value
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=NotificationLiteral.SOMETHING_WENT_WRONG
        )
    return updated_notification


@notification_router.delete(
    path="/{notification_id}",
    tags=[constants.NotificationLiteral.TAGS],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_notification(
    notification_id: Annotated[int, Path(gt=0)],
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
):
    try:
        notification_service.delete(notification_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NotificationLiteral.NOTIFICATION_NOT_FOUND.value
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=NotificationLiteral.SOMETHING_WENT_WRONG
        )
