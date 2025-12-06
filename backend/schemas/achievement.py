from pydantic import BaseModel


class AchievementDTO(BaseModel):
    id: int
    name: str
    description: str
    division: str
    kpi: str
    reward: int
    position: str
    period: str

    class Config:
        from_attributes = True


class AchievementsList(BaseModel):
    achievements: list[AchievementDTO]


class PatchAchievementDTO(BaseModel):
    name: str | None = None
    description: str | None = None
    division: str | None = None
    kpi: str | None = None
    reward: int | None = None
    position: str | None = None
    period: str | None = None
