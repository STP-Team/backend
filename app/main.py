from fastapi import FastAPI, Request
from stp_database import create_engine, create_session_pool
from stp_database.repo.STP import MainRequestsRepo

from app.core.config import load_config
from app.api.employees import router as employees_router
from app.api.achievements import router as achievements_router

config = load_config(".env")

engine = create_engine(config.db, db_name=config.db.db_name)
session_pool = create_session_pool(engine)


app = FastAPI()
app.include_router(employees_router)
app.include_router(achievements_router)


@app.middleware("http")
async def add_repo(request: Request, call_next):
    async with session_pool() as session:
        request.state.repo = MainRequestsRepo(session)
        response = await call_next(request)
        return response


@app.middleware("http")
async def add_session(request: Request, call_next):
    async with session_pool() as async_session:
        request.state.session = async_session
        response = await call_next(request)
        return response


@app.get("/health")
async def read_health():
    return {"status": "ok"}
