from fastapi import FastAPI

from app.routers import user_router
from infra.config import settings

app = FastAPI(title=settings.app_name)


app.include_router(user_router.router)
