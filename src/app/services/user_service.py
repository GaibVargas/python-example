from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.user_dtos import UserCreate, UserUpdate
from app.models.user_model import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = UserRepository(db)

    async def create_user(self, payload: UserCreate) -> User:
        existing = self.repo.get_by_cpf(payload.cpf)
        if existing:
            raise ValueError("User with this CPF already exists")
        return await self.repo.create(payload)

    async def get_user(self, cpf: str) -> User | None:
        return await self.repo.get_by_cpf(cpf)

    async def update_user(self, cpf: str, payload: UserUpdate) -> User | None:
        user = await self.repo.get_by_cpf(cpf)
        if not user:
            return None
        return await self.repo.update(user, payload)
