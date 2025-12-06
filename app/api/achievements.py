from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import ValidationError

from app.core.db import RepoDep
from app.schemas.achievement import AchievementDTO, AchievementsList
from app.schemas.employee import PatchEmployeeDTO

router = APIRouter(prefix="/api/achievements", tags=["Достижения"])


@router.get(
    "/",
    name="Получить достижения",
    description="Получает список достижений с фильтрами",
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request"},
    },
    response_model=AchievementsList,
)
async def get_achievements(
    repo: RepoDep,
    division: str | None = Query(None, description="Направление сотрудника"),
    achievement_id: int | None = Query(None, description="Идентификатор достижения"),
):
    try:
        achievements = await repo.achievement.get_achievements(
            achievement_id=achievement_id, division=division
        )

        if not achievements:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )

        if not isinstance(achievements, (list, tuple)):
            achievements = [achievements]

        achievements = [AchievementDTO.model_validate(ach) for ach in achievements]

        return AchievementsList(achievements=achievements)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error: {e}",
        ) from e


@router.post(
    "/",
    name="Создать достижение",
    description="Создает новое достижение",
    status_code=status.HTTP_201_CREATED,
    response_model=AchievementDTO,
)
async def create_achievement(
    request: Request,
    repo: RepoDep,
    name: str = Query(str, description="Название достижения"),
    description: str = Query(str, description="Название достижения"),
    division: str = Query(
        str, description="Направление сотрудника (НТП/НЦК) для получения достижения"
    ),
    kpi: str = Query(str, description="Показатели KPI для получения достижения"),
    reward: int = Query(int, description="Награда за получение достижение в баллах"),
    position: str = Query(
        str, description="Позиция/должность сотрудника для получения достижения"
    ),
    period: str = Query(
        str,
        description="Частота возможного получения достижения: день, неделя, месяц и ручная",
    ),
):
    try:
        achievement = await repo.achievement.add_achievement(
            name=name,
            description=description,
            division=division,
            kpi=kpi,
            reward=reward,
            position=position,
            period=period,
        )

        if not achievement:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось создать достижение",
            )

        return achievement

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка валидации входных данных: {e}",
        ) from e

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url.path),
                "message": "Внутренняя ошибка сервера при создании достижения",
                "errorCode": "INTERNAL_SERVER_ERROR",
            },
        ) from None


@router.patch(
    "/",
    name="Изменить достижение",
    description="Изменяет существующее достижение",
    status_code=status.HTTP_200_OK,
    response_model=AchievementDTO,
)
async def patch_achievement(
    request: Request,
    repo: RepoDep,
    payload: PatchEmployeeDTO,
    achievement_id: int = Query(int, description="Идентификатор достижения"),
):
    try:
        achievement = await repo.achievement.get_achievements(
            achievement_id=achievement_id
        )

        if not achievement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )

        update_data = payload.model_dump(exclude_unset=True)
        updated = await repo.achievement.update_achievement(
            achievement_id, **update_data
        )

        return updated
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка валидации входных данных: {e}",
        ) from e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url.path),
                "message": "Внутренняя ошибка сервера при обновлении достижения",
                "errorCode": "INTERNAL_SERVER_ERROR",
            },
        ) from None


@router.delete(
    "/",
    name="Удалить достижение",
    status_code=status.HTTP_200_OK,
)
async def delete_achievement(
    request: Request,
    repo: RepoDep,
    achievement_id: int | None = Query(None, description="Идентификатор достижения"),
):
    try:
        deleted = await repo.achievement.delete_achievement(
            achievement_id=achievement_id
        )

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error deleting achievement",
            )

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка валидации входных данных: {e}",
        ) from e

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url.path),
                "message": "Внутренняя ошибка сервера при удалении сотрудника",
                "errorCode": "INTERNAL_SERVER_ERROR",
            },
        ) from None
