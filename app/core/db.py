from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from stp_database import create_engine, create_session_pool
from stp_database.repo.STP import MainRequestsRepo

from app.core.config import settings

engine = create_engine(
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    username=settings.DB_USER,
    password=settings.DB_PASS,
    db_name=settings.DB_NAME,
)
session_pool = create_session_pool(engine)


async def get_session():
    async with session_pool() as session:
        yield session


async def get_repo():
    async with session_pool() as session:
        yield MainRequestsRepo(session)


SessionDep = Annotated[AsyncSession, Depends(get_session)]
RepoDep = Annotated[MainRequestsRepo, Depends(get_repo)]
