from fastapi import APIRouter, Depends
from stp_database.repo.STP import MainRequestsRepo

from app.core.dependencies import get_repo

router = APIRouter(prefix="/api/achievements", tags=["Achievements"])


@router.get("/")
async def get_achievements(
    repo: MainRequestsRepo = Depends(get_repo),
):
    achievements = await repo.achievement.get_achievements()

    if not achievements:
        return {"error": "Not found"}

    return {"achievements": achievements}


@router.get("/{achievement_id}")
async def get_achievement(
    achievement_id: int, repo: MainRequestsRepo = Depends(get_repo)
):
    achievement = await repo.achievement.get_achievements(achievement_id=achievement_id)

    if not achievement:
        return {"error": "Not found"}

    return {"achievement": achievement}
