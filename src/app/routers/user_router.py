from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.user_dtos import UserCreate, UserRead, UserUpdate
from app.models.user_model import User
from app.services.user_service import UserService
from infra.db import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    svc = UserService(db)
    try:
        return await svc.create_user(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/{cpf}", response_model=UserRead)
async def get_user(cpf: str, db: AsyncSession = Depends(get_db)) -> User:
    svc = UserService(db)
    user = await svc.get_user(cpf)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{cpf}", response_model=UserRead)
async def update_user(
    cpf: str, payload: UserUpdate, db: AsyncSession = Depends(get_db)
) -> User:
    svc = UserService(db)
    updated = await svc.update_user(cpf, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated
