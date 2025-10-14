from enum import Enum

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(str, Enum):
    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    exception = "exception"


class Enviroment(str, Enum):
    development = "development"
    production = "production"
    test = "test"


class Settings(BaseSettings):
    app_name: str = Field("FastAPI App", description="Nome da aplicação")
    environment: Enviroment = Field(
        Enviroment.development, description="Ambiente de execução"
    )
    debug: bool = Field(True, description="Modo debug habilitado ou não")
    log_level: LogLevel = Field(LogLevel.info, description="Nível de log da aplicação")

    postgres_user: str = Field(..., description="Usuário do banco de dados")
    postgres_password: str = Field(..., description="Senha do banco de dados")
    postgres_host: str = Field("localhost", description="Host do banco de dados")
    postgres_port: int = Field(5432, description="Porta do banco de dados")
    postgres_db: str = Field(..., description="Nome do banco de dados")

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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


# Existe somente para que load_settings faça a inferência correta do tipo
def _load_settings() -> Settings:
    return Settings()


def load_settings() -> Settings:
    try:
        return _load_settings()
    except ValidationError as e:
        print("\nErro ao carregar variáveis de ambiente:\n")
        for error in e.errors():
            loc = ".".join(map(str, error["loc"]))
            msg = error["msg"]
            print(f"  - {loc}: {msg}")
        print("\nVerifique o arquivo .env ou as variáveis do ambiente.\n")
        raise RuntimeError("System environment is not properly configured.")


settings = load_settings()
