from typing import Annotated

from fastapi import APIRouter, Path, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from notifications import constants
from notifications.constants import NotificationLiteral
from notifications.schemas import Notification, BodyNotification, RepeatInterval
from notifications.service import NotificationService
from database import get_db


notification_router = APIRouter(prefix="/notifications")


fake_data_notifications = {
    1: Notification(id=1, title="title-1", body="body-1", repeat_interval=RepeatInterval(how_often=constants.RepeatInterval.ONCE.value, step=0)),
    2: Notification(id=2, title="title-2", body="body-2", repeat_interval=RepeatInterval(how_often=constants.RepeatInterval.DAILY.value, step=1)),
    3: Notification(id=3, title="title-3", body="body-3", repeat_interval=RepeatInterval(how_often=constants.RepeatInterval.MONTHLY.value, step=0)),
}


@notification_router.get(
    path="/",
    tags=[NotificationLiteral.TAGS],
    response_model=list[Notification]
)
async def list_notifications(database: Annotated[Session, Depends(get_db)]):
    notification_service = NotificationService(database)
    return notification_service.get_list()


@notification_router.post(
    path="/",
    tags=[NotificationLiteral.TAGS],
    status_code=status.HTTP_201_CREATED,
    response_model=Notification
)
async def create_notification(
    notification: BodyNotification,
    database: Annotated[Session, Depends(get_db)]
) -> Notification:
    notification_service = NotificationService(database)
    try:
        created_notification = notification_service.create(notification)
    except Exception as err:
        # here should be logging for the error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, please try again later"
        )
    return created_notification

@notification_router.get(
    path="/{notification_id}",
    tags=[constants.NotificationLiteral.TAGS],
    response_model=Notification
)
async def get_notification(
    notification_id: Annotated[int, Path(gt=0)],
    database: Annotated[Session, Depends(get_db)],
):
    service = NotificationService(database)
    return service.get_by_id(notification_id)


@notification_router.put(
    path="/{notification_id}",
    tags=[constants.NotificationLiteral.TAGS],
    response_model=Notification
)
async def update_notification(
    notification_id: Annotated[int, Path(gt=0)],
    notification: BodyNotification,
    database: Annotated[Session, Depends(get_db)],
):
    service = NotificationService(database)
    return service.update(notification_id, notification)


@notification_router.delete(
    path="/{notification_id}",
    tags=[constants.NotificationLiteral.TAGS],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_notification(
    notification_id: Annotated[int, Path(gt=0)],
    database: Annotated[Session, Depends(get_db)],
):
    service = NotificationService(database)
    service.delete(notification_id)