from pathlib import Path
from typing import Annotated, Any

from pydantic import AnyUrl, BaseModel, BeforeValidator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "EdDSA"


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI App"
    OPENAPI_URL: str = "/openapi.json"
    API_V1_STR: str = "/api/v1"
    FRONTEND_HOST: str = "http://localhost:3000"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    auth_jwt: AuthJWT = AuthJWT()

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_NAME: str = "app_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        strict=True,
    )


settings = Settings()
