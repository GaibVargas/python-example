from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["UP", "DOWN"]


class ReadinessResponse(BaseModel):
    status: Literal["READY", "NOT_READY"]


class InfoResponse(BaseModel):
    name: str
    env: str
    version: str
    commit: str
    build_time: str
