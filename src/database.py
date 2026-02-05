from collections.abc import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import DatabaseSettings, CommonSettings

database_settings = DatabaseSettings()

DATABASE_URL = f"{database_settings.DATABASE_ASYNC_DRIVER}://{database_settings.DATABASE_USER}:{database_settings.DATABASE_PASSWORD}@{database_settings.DATABASE_HOST}:{database_settings.DATABASE_PORT}/{database_settings.DATABASE_NAME}"

common_settings = CommonSettings()

engine_parameters = {
    "pool_pre_ping": True,
}

if common_settings.DEBUG:
    engine_parameters["echo"] = True

engine = create_async_engine(DATABASE_URL, **engine_parameters)

constraint_naming_conventions = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=constraint_naming_conventions)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)

async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as database_session:
        try:
            yield database_session
            await database_session.commit()
        except Exception:
            await database_session.rollback()
            raise
