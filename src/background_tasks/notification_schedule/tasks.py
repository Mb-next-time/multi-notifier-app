import asyncio
import logging
from typing import Annotated, Sequence, Any

from fastapi import Depends
from sqlalchemy import select, RowMapping, and_
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from background_tasks import broker
from background_tasks.schemas import NotificationAggregate
from database import get_database_session, default_datetime
from notification_schedule.models import NotificationSchedule
from notifications.models import Notification
from channels.models import Channel
from background_tasks.models import NotificationDelivery

logger = logging.getLogger(__name__)


@broker.task
async def send_notification(
    notification_aggregate: NotificationAggregate,
    database_session: Annotated[AsyncSession,Depends(get_database_session)],
) -> None:
    new_notification_delivery: dict[str, Any] = {
        "notification_schedule_id": notification_aggregate.notification_schedule_id,
        "channel": {
            "channel_id": notification_aggregate.channel_id,
            "provider": notification_aggregate.provider,
            "destination": notification_aggregate.destination,
        },
        "notification": {
            "notification_id": notification_aggregate.notification_id,
            "title": notification_aggregate.title,
            "body": notification_aggregate.body,
            "repeat_settings": notification_aggregate.repeat_settings.model_dump(),
        },
        "next_fire_at": notification_aggregate.next_fire_at,
    }
    constraint: str = "uq_notification_delivery_notification_schedule_id_next_fire_at"
    statement = None
    try:
        # sending to email provider
        # raise Exception("Sending is failed")
        await asyncio.sleep(1)
        statement = pg_insert(NotificationDelivery).values(
            **new_notification_delivery,
            status="success"
        ).on_conflict_do_update(
            constraint=constraint,
            set_={
                "status": "success",
                "delivered_at": default_datetime()
            },
        )
    except Exception as e:
        logger.error(f"send_notification: {notification_aggregate=}, error: {e}")
        statement = pg_insert(NotificationDelivery).values(
            **new_notification_delivery,
            status="failed",
            current_attempt=2
        ).on_conflict_do_update(
            constraint=constraint,
            set_={
                "status": "failed",
                "current_attempt": NotificationDelivery.current_attempt + 1,
                "error_message": str(e),
            },
            where=(NotificationDelivery.current_attempt < 5)
        ).returning(NotificationDelivery.id)

    await database_session.execute(statement)
    # result = (await database_session.execute(statement)).first()
    # if result:
    #     await send_notification.kicker().with_labels(delay=30).kiq(notification_aggregate)

@broker.task(schedule=[{"cron": "* * * * *"}])
async def prepare_notifications_to_sending(database_session: Annotated[AsyncSession,Depends(get_database_session)]) -> None:
    logger.info("Sending notifications")
    statement = select(
        NotificationSchedule.id.label("notification_schedule_id"),
        NotificationSchedule.next_fire_at,
        NotificationSchedule.repeat_settings,
        Notification.id.label("notification_id"),
        Notification.title,
        Notification.body,
        Channel.id.label("channel_id"),
        Channel.provider,
        Channel.destination,
    ).join(
        NotificationSchedule, NotificationSchedule.notification_id == Notification.id
    ).join(
        Channel, NotificationSchedule.channel_id == Channel.id
    ).with_for_update(skip_locked=True).limit(5)
    notification_aggregates: Sequence[RowMapping] = (await database_session.execute(statement)).mappings().all()
    for notification_aggregate in notification_aggregates:
        await send_notification.kiq(NotificationAggregate(**notification_aggregate))
    # calculate a new "next_fire_at" and update NotificationSchedule

