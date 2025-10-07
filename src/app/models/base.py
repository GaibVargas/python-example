from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base for SQLAlchemy models."""

    pass

# Necessário para alembic funcionar corretamente
from . import user_model  # noqa: E402, F401
