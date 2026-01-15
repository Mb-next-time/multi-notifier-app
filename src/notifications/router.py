from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Path, status, HTTPException

from notifications.schemas import Notification, BodyNotification

api = APIRouter(prefix="/notifications")


fake_data_notifications = {
    1: Notification(id=1, title="title-1", body="body-1", interval=10),
    2: Notification(id=2, title="title-2", body="body-2", interval=0),
    3: Notification(id=3, title="title-3", body="body-3", interval=5),
}


@api.get(
    path="/",
    tags=["notifications"],
    response_model=list[Notification]
)
async def list_notifications():
    return fake_data_notifications.values()


@api.post(
    path="/",
    tags=["notifications"],
    status_code=status.HTTP_201_CREATED,
    response_model=Notification
)
async def create_notification(notification: BodyNotification) -> Notification:
    new_notification = Notification(
        id=4,
        title=notification.title,
        body=notification.body,
        interval=notification.interval,
    )
    return new_notification


@api.put(
    path="/{notification_id}",
    tags=["notifications"],
    response_model=Notification
)
async def update_notification(notification_id: Annotated[int, Path(gt=0)], notification: BodyNotification):
    if notification_id not in fake_data_notifications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    updated_notification = notification.model_copy(update={"id": notification.id})
    return updated_notification


@api.delete(
    path="/{notification_id}",
    tags=["notifications"],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_notification(notification_id: Annotated[int, Path(gt=0)]):
    if notification_id not in fake_data_notifications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # remove from database the entity