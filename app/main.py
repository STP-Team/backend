import uvicorn
from fastapi import FastAPI

from .api import routers
from .core.config import load_config

config = load_config(".env")

app = FastAPI()

app.add_middleware(
    allow_origins=[
        "http://test.lab.loc",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=config.api.port, reload=True)
