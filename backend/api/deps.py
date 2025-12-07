from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from stp_database import create_session_pool
from stp_database.models.STP import Employee
from stp_database.repo.STP import MainRequestsRepo

from backend.auth.utils import decode_jwt
from backend.core.db import engine

session_pool = create_session_pool(engine)


async def get_session():
    async with session_pool() as session:
        yield session


async def get_repo():
    async with session_pool() as session:
        yield MainRequestsRepo(session)


SessionDep = Annotated[AsyncSession, Depends(get_session)]
RepoDep = Annotated[MainRequestsRepo, Depends(get_repo)]
security = HTTPBearer()


async def get_current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    repo: RepoDep,
):
    """Validate JWT token and return current user"""
    try:
        payload = await decode_jwt(token.credentials)
        user_id: int | None = payload.get("user_id", None)

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

        users = await repo.employee.get_users(user_id=user_id)
        if not users:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        user = users[0] if isinstance(users, list) else users
        return user

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


CurrentUserDep = Annotated[Employee, Depends(get_current_user)]
