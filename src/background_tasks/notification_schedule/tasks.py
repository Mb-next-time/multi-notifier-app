import asyncio
import logging
from typing import Annotated, Sequence, Any

from fastapi import Depends
from sqlalchemy import select, RowMapping, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from background_tasks import broker
from background_tasks.schemas import NotificationAggregate, ResultOfSendNotification
from background_tasks.notification_schedule.constants import (
    NotificationDeliveryStatus, MAX_DELIVERY_ATTEMPTS, NUMBER_OF_NOTIFICATIONS_TO_SEND
)
from background_tasks.notification_schedule.utils import factory_relativedelta
from background_tasks.models import NotificationDelivery
from background_tasks.notification_schedule.constants import NotificationDeliveryLiteral
from database import get_database_session, current_datetime_utc
from notification_schedule.models import NotificationSchedule
from notification_schedule.constants import NotificationScheduleLiteral, RepeatInterval, NotificationScheduleStatus
from notification_schedule.schemas import RepeatSettings
from notifications.models import Notification
from notifications.constants import NotificationLiteral, NotificationSchemeField
from channels.models import Channel
from channels.constants import ChannelLiteral, ChannelSchemeField


logger = logging.getLogger(__name__)

@broker.task
async def send_notification(
    notification_aggregate: NotificationAggregate,
    database_session: Annotated[AsyncSession,Depends(get_database_session)],
) -> None:
    new_notification_delivery: dict[str, Any] = {
        NotificationScheduleLiteral.NOTIFICATION_SCHEDULE_ID.value: notification_aggregate.notification_schedule_id,
        "channel": {
            ChannelLiteral.CHANNEL_ID.value: notification_aggregate.channel_id,
            ChannelSchemeField.PROVIDER.value: notification_aggregate.provider,
            ChannelSchemeField.DESTINATION.value: notification_aggregate.destination,
        },
        "notification": {
            NotificationLiteral.NOTIFICATION_ID.value: notification_aggregate.notification_id,
            NotificationSchemeField.TITLE.value: notification_aggregate.title,
            NotificationSchemeField.BODY.value: notification_aggregate.body,
            NotificationScheduleLiteral.REPEAT_SETTINGS.value: notification_aggregate.repeat_settings.model_dump(),
        },
        NotificationScheduleLiteral.NEXT_FIRE_AT.value: notification_aggregate.next_fire_at,
    }

    result = ResultOfSendNotification(
        code=NotificationDeliveryStatus.SUCCESS.value,
        error=None
    )
    try:
        # fake sending to email provider
        # raise Exception("Email Service is failed")
        await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"{notification_aggregate=}, error: {e}")
        result.code = NotificationDeliveryStatus.FAILED.value
        result.error = str(e)

    constraint: str = f"uq_notification_delivery_{NotificationScheduleLiteral.NOTIFICATION_SCHEDULE_ID.value}_{NotificationScheduleLiteral.NEXT_FIRE_AT.value}"
    statement = None

    if result.code == NotificationDeliveryStatus.SUCCESS.value:
        statement = pg_insert(NotificationDelivery).values(
            **new_notification_delivery,
            status=NotificationDeliveryStatus.SUCCESS.value,
        ).on_conflict_do_update(
            constraint=constraint,
            set_={
                NotificationDeliveryLiteral.STATUS.value: NotificationDeliveryStatus.SUCCESS.value,
                NotificationDeliveryLiteral.DELIVERED_AT.value: current_datetime_utc()
            },
        )
    elif result.code == NotificationDeliveryStatus.FAILED.value:
        statement = pg_insert(NotificationDelivery).values(
            **new_notification_delivery,
            status=NotificationDeliveryStatus.FAILED.value,
            current_attempt=2,
            error_message=result.error,
        ).on_conflict_do_update(
            constraint=constraint,
            set_={
                NotificationDeliveryLiteral.STATUS.value: NotificationDeliveryStatus.FAILED.value,
                NotificationDeliveryLiteral.CURRENT_ATTEMPT.value: NotificationDelivery.current_attempt + 1,
                NotificationDeliveryLiteral.ERROR_MESSAGE.value: result.error,
            },
            where=(NotificationDelivery.current_attempt < MAX_DELIVERY_ATTEMPTS)
        ).returning(NotificationDelivery.id)

    result = (await database_session.execute(statement)).first()

    # Should set up retry messages and delayed time
    # if result:
    #     await send_notification.kicker().with_labels(delay=30).kiq(notification_aggregate)

@broker.task(schedule=[{"cron": "*/2 * * * *"}])
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
    notification_aggregates: Sequence[RowMapping] = (await database_session.execute(statement)).mappings().all()

    for notification_aggregate_row_mapping in notification_aggregates:
        notification_aggregate = NotificationAggregate(**notification_aggregate_row_mapping)
        await send_notification.kiq(notification_aggregate)
        # to do refactoring
        update_data = {}
        repeat_settings: RepeatSettings = notification_aggregate.repeat_settings
        if repeat_settings.how_often == RepeatInterval.ONCE.value:
            update_data[NotificationScheduleLiteral.STATUS.value] = NotificationScheduleStatus.DONE.value
        else:
            update_data[
                NotificationScheduleLiteral.NEXT_FIRE_AT.value
            ] = notification_aggregate.next_fire_at + factory_relativedelta(repeat_settings.how_often, repeat_settings.step)

        await database_session.execute(update(NotificationSchedule).values(**update_data)
        .where(NotificationSchedule.id == notification_aggregate.notification_schedule_id))
