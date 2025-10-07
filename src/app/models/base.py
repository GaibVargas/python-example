from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base for SQLAlchemy models."""

    pass


from . import user_model  # noqa: E402, F401
