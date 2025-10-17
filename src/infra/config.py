import tomllib as tomli
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Tuple

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from infra.logger.logger_level import LogLevel


class Enviroment(str, Enum):
    development = "development"
    production = "production"
    test = "test"


class Settings(BaseSettings):
    app_name: str | None = Field(
        None, description="Nome da aplicação"
    )  # set from pyproject.toml
    app_host: str = Field(..., description="Host da aplicação")
    app_port: int = Field(8000, description="Porta da aplicação")
    app_version: str | None = Field(
        None, description="Versão da aplicação"
    )  # set from pyproject.toml
    commit: str = Field(
        "N/A", description="Hash do commit da aplicação"
    )  # set in CI/CD
    build_time: str | None = Field(
        None, description="Data e hora da build da aplicação"
    )  # set in CI/CD
    environment: Enviroment = Field(
        Enviroment.development, description="Ambiente de execução"
    )
    debug: bool = Field(True, description="Modo debug habilitado ou não")
    log_level: LogLevel = Field(LogLevel.info, description="Nível de log da aplicação")

    postgres_user: str = Field(..., description="Usuário do banco de dados")
    postgres_password: str = Field(..., description="Senha do banco de dados")
    postgres_host: str = Field(..., description="Host do banco de dados")
    postgres_port: int = Field(5432, description="Porta do banco de dados")
    postgres_db: str = Field(..., description="Nome do banco de dados")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def sync_database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


def get_app_info_from_pyproject() -> Tuple[str, str]:
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    if not pyproject_path.exists():
        return "N/A", "0.1.0"
    with pyproject_path.open("rb") as f:
        data = tomli.load(f)
        return data.get("project", {}).get("name", "N/A"), data.get("project", {}).get(
            "version", "0.1.0"
        )


# Existe somente para que load_settings faça a inferência correta do tipo
def _load_settings() -> Settings:
    return Settings()


def load_settings() -> Settings:
    try:
        settings = _load_settings()

        if not settings.app_name or not settings.app_version:
            name, version = get_app_info_from_pyproject()
            settings.app_name = name
            settings.app_version = version

        if not settings.build_time:
            settings.build_time = datetime.now(timezone.utc).isoformat() + "Z"

        return settings
    except ValidationError as e:
        print("\nErro ao carregar variáveis de ambiente:\n")
        for error in e.errors():
            loc = ".".join(map(str, error["loc"]))
            msg = error["msg"]
            print(f"  - {loc}: {msg}")
        print("\nVerifique o arquivo .env ou as variáveis do ambiente.\n")
        raise RuntimeError("System environment is not properly configured.")


settings = load_settings()
