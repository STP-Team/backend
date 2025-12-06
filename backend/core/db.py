from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from stp_database import create_engine, create_session_pool
from stp_database.repo.STP import MainRequestsRepo

from backend.core.config import load_config

config = load_config(".env")
engine = create_engine(config.db, db_name=config.db.db_name)
session_pool = create_session_pool(engine)


async def get_session():
    async with session_pool() as session:
        yield session


async def get_repo():
    async with session_pool() as session:
        yield MainRequestsRepo(session)


SessionDep = Annotated[AsyncSession, Depends(get_session)]
RepoDep = Annotated[MainRequestsRepo, Depends(get_repo)]
