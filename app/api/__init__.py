from .achievements import router as achievements_router
from .employees import router as employees_router

routers = [
    employees_router,
    achievements_router,
]

__all__ = [
    "routers",
]
