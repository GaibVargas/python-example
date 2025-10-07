from sqlalchemy import Column, Integer, String

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, unique=True, nullable=False, index=True)
    nickname = Column(String, nullable=True)
    full_name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
