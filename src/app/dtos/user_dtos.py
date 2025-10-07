from pydantic import BaseModel


class UserCreate(BaseModel):
    cpf: str
    full_name: str
    nickname: str | None = None
    age: int | None = None


class UserUpdate(BaseModel):
    full_name: str | None = None
    nickname: str | None = None
    age: int | None = None


class UserRead(BaseModel):
    id: int
    cpf: str
    full_name: str
    nickname: str | None = None
    age: int | None = None
