from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.user_dtos import UserCreate, UserUpdate
from app.models.user_model import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_cpf(self, cpf: str) -> User | None:
        stmt = select(User).where(User.cpf == cpf)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, payload: UserCreate) -> User:
        user = User(**payload.model_dump())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user: User, payload: UserUpdate) -> User:
        data = payload.model_dump(exclude_unset=True)
        data.pop("cpf", None)

        for key, value in data.items():
            setattr(user, key, value)

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
