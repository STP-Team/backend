import uvicorn
from fastapi import FastAPI

from backend.api import routers
from backend.core.config import load_config

config = load_config(".env")

app = FastAPI()

for router in routers:
    app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=config.api.port, reload=True)
