from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from stp_database.repo.STP import MainRequestsRepo


def get_repo(request: Request) -> MainRequestsRepo:
    return request.state.repo


def get_session(request: Request) -> AsyncSession:
    return request.state.session
