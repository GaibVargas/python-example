from typing import Dict
from fastapi import FastAPI

from app.routers import user_router
from infra.config import settings

app = FastAPI(title=settings.app_name)


@app.get("/health", tags=["health"])
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


app.include_router(user_router.router)
