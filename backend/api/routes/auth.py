from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from backend.api.deps import CurrentUserDep, RepoDep
from backend.auth.utils import encode_jwt, validate_telegram_auth
from backend.core.config import settings
from backend.schemas.auth import TelegramAuthData, TokenInfo, UserInfo

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)


@router.post("/telegram", name="Авторизация через Telegram", response_model=TokenInfo)
async def auth_telegram(auth_data: TelegramAuthData, repo: RepoDep):
    """
    Authenticate user via Telegram Login Widget

    This endpoint validates Telegram authentication data and returns a JWT token.
    The auth_data must contain valid Telegram widget data including hash for verification.
    """

    # Convert Pydantic model to dict for validation
    auth_dict = auth_data.model_dump()

    # Validate Telegram authentication
    if not validate_telegram_auth(auth_dict, settings.TELEGRAM_BOT_TOKEN):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Telegram authentication data",
        )

    # Check authentication timestamp (optional - within last 24 hours)
    try:
        auth_timestamp = int(auth_data.auth_date)
        current_timestamp = int(datetime.now().timestamp())
        if current_timestamp - auth_timestamp > 86400:  # 24 hours
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication data expired",
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid auth_date format"
        )

    # Get user by Telegram ID
    telegram_user_id = int(auth_data.id)
    users = await repo.employee.get_users(user_id=telegram_user_id)

    if not users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found in database",
        )

    user = users[0] if isinstance(users, list) else users

    if user.role != 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )

    jwt_payload = {
        "sub": str(user.user_id),
        "user_id": user.user_id,
        "fullname": user.fullname,
        "role": user.role,
    }
    access_token = await encode_jwt(payload=jwt_payload)

    return TokenInfo(access_token=access_token, token_type="Bearer")


@router.get(
    "/me", name="Получить информацию о текущем пользователе", response_model=UserInfo
)
async def get_current_user_info(current_user: CurrentUserDep):
    """Get current user information by token"""
    return UserInfo(
        user_id=current_user.user_id,
        fullname=current_user.fullname,
        role=current_user.role,
        username=getattr(current_user, "username", None),
        division=getattr(current_user, "division", None),
        position=getattr(current_user, "position", None),
    )
