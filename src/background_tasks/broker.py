import taskiq_fastapi
from taskiq import TaskiqScheduler, SmartRetryMiddleware
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker, Queue

from background_tasks.config import BrokerSettings

broker_settings = BrokerSettings()

broker = AioPikaBroker(
    url=f'{broker_settings.PROTOCOL}://{broker_settings.USERNAME}:{broker_settings.PASSWORD}@{broker_settings.HOSTNAME}:{broker_settings.PORT}',
    delay_queue=Queue(
        name="taskiq.delay_queue",
        durable=True,
        arguments={
            "x-queue-type": "classic",
            "x-dead-letter-exchange": "taskiq",
            "x-dead-letter-routing-key": "taskiq",
        },
    ),
).with_middlewares(SmartRetryMiddleware(
        default_retry_count=5,
        default_delay=10,
        use_jitter=True,
        use_delay_exponent=True,
        max_delay_exponent=180
    ))

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)

taskiq_fastapi.init(broker, "main:app")
