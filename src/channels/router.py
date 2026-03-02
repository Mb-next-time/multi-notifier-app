from typing import Annotated

from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_authenticated_user
from auth.models import User
from channels.constants import ChannelLiteral
from channels.models import Channel
from channels.schemas import BodyChannel, ResponseChannel
from database import get_database_session


channel_router = APIRouter(prefix=f"/{ChannelLiteral.URL.value}", tags=[ChannelLiteral.TAGS])

@channel_router.get(
    path="/",
    response_model=list[ResponseChannel]
)
async def list_channels(
    database_session: Annotated[AsyncSession,Depends(get_database_session)],
    user: Annotated[User, Depends(get_current_authenticated_user)]
):
    channels = (await database_session.execute(select(Channel).where(Channel.user_id == user.id))).scalars().all()
    return channels

@channel_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseChannel
)
async def create_channel(
    channel: BodyChannel,
    database_session: Annotated[AsyncSession, Depends(get_database_session)],
    user: Annotated[User, Depends(get_current_authenticated_user)]
):
    channel_in_db = Channel(
        provider=channel.provider,
        destination=channel.destination,
        user_id=user.id,
    )
    try:
        database_session.add(channel_in_db)
        await database_session.flush()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Channel already exists"
        )
    return channel_in_db
