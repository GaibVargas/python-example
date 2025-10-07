from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.user_dependencies import get_user_service
from app.dtos.user_dtos import UserCreate, UserRead, UserUpdate
from app.models.user_model import User
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
async def create_user(
    payload: UserCreate, svc: UserService = Depends(get_user_service)
) -> User:
    try:
        return await svc.create_user(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/{cpf}", response_model=UserRead)
async def get_user(cpf: str, svc: UserService = Depends(get_user_service)) -> User:
    user = await svc.get_user(cpf)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{cpf}", response_model=UserRead)
async def update_user(
    cpf: str, payload: UserUpdate, svc: UserService = Depends(get_user_service)
) -> User:
    updated = await svc.update_user(cpf, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated
