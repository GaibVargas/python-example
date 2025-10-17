from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.observability_dtos import HealthResponse, InfoResponse, ReadinessResponse
from app.routers import user_router
from infra.config import settings
from infra.db import get_db

app = FastAPI(title=settings.app_name or "FastAPI Application")


@app.get("/health", tags=["observability"])
async def healthcheck() -> HealthResponse:
    return HealthResponse(status="UP")


@app.get("/ready", tags=["observability"])
async def readiness_check(db: AsyncSession = Depends(get_db)) -> ReadinessResponse:
    try:
        await db.execute(text("SELECT 1"))
        return ReadinessResponse(status="READY")
    except Exception:
        return ReadinessResponse(status="NOT_READY")


@app.get("/info", tags=["observability"])
async def info_check() -> InfoResponse:
    return InfoResponse(
        name=settings.app_name,
        env=settings.environment,
        version=settings.app_version,
        commit=settings.commit,
        build_time=settings.build_time,
    )


app.include_router(user_router.router)
