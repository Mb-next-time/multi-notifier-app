import asyncio
import logging
from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy import select, RowMapping, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqError

from background_tasks import broker
from background_tasks.schemas import NotificationAggregate
from background_tasks.notification_schedule.constants import (
    MAX_DELIVERY_ATTEMPTS, NUMBER_OF_NOTIFICATIONS_TO_SEND
)
from background_tasks.notification_schedule.utils import factory_relativedelta
from database import get_database_session, current_datetime_utc
from notification_schedule.models import NotificationSchedule
from notification_schedule.constants import NotificationScheduleLiteral, RepeatInterval, NotificationScheduleStatus
from notification_schedule.schemas import RepeatSettings
from notifications.models import Notification
from notifications.constants import NotificationLiteral
from channels.models import Channel
from channels.constants import ChannelLiteral


logger = logging.getLogger(__name__)

@broker.task(
    retry_on_error=True,
    max_retries=MAX_DELIVERY_ATTEMPTS
)
async def send_notification(
    notification_aggregate: NotificationAggregate
) -> None:

    try:
        # fake error
        # raise Exception("Email Service is failed")
        # fake sending to email provider
        await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"{notification_aggregate=}, error: {e}")
        raise


@broker.task(schedule=[{"cron": "* * * * *"}])
async def prepare_notifications_to_sending(database_session: Annotated[AsyncSession,Depends(get_database_session)]) -> None:
    statement = (select(
        NotificationSchedule.id.label(NotificationScheduleLiteral.NOTIFICATION_SCHEDULE_ID.value),
        NotificationSchedule.next_fire_at,
        NotificationSchedule.repeat_settings,
        Notification.id.label(NotificationLiteral.NOTIFICATION_ID.value),
        Notification.title,
        Notification.body,
        Channel.id.label(ChannelLiteral.CHANNEL_ID.value),
        Channel.provider,
        Channel.destination
    ).join(
        NotificationSchedule, NotificationSchedule.notification_id == Notification.id
    ).join(
        Channel, NotificationSchedule.channel_id == Channel.id
    ).where(
        NotificationSchedule.status == NotificationScheduleStatus.RUNNING.value,
        NotificationSchedule.next_fire_at <= current_datetime_utc()
    ).with_for_update(skip_locked=True).limit(NUMBER_OF_NOTIFICATIONS_TO_SEND))

    notification_aggregates = []
    try:
        notification_aggregates: Sequence[RowMapping] = (await database_session.execute(statement)).mappings().all()
    except SQLAlchemyError as error:
        logger.error(str(error))

    for notification_aggregate_row_mapping in notification_aggregates:
        notification_aggregate = NotificationAggregate(**notification_aggregate_row_mapping)
        try:
            await send_notification.kicker().kiq(notification_aggregate)
        except TaskiqError as error:
            logger.error(str(error))
            return

        update_data = {}
        repeat_settings: RepeatSettings = notification_aggregate.repeat_settings
        if repeat_settings.how_often == RepeatInterval.ONCE.value:
            update_data[NotificationScheduleLiteral.STATUS.value] = NotificationScheduleStatus.DONE.value
        else:
            update_data[
                NotificationScheduleLiteral.NEXT_FIRE_AT.value
            ] = notification_aggregate.next_fire_at + factory_relativedelta(repeat_settings.how_often, repeat_settings.step)

        try:
            await database_session.execute(update(NotificationSchedule).values(**update_data)
            .where(NotificationSchedule.id == notification_aggregate.notification_schedule_id))
        except SQLAlchemyError as error:
            logger.error(str(error))
            raise
