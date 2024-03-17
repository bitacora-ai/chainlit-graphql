import secrets
import warnings
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, model_validator, computed_field
from typing import Literal, Optional
from pydantic_core import MultiHostUrl
from typing_extensions import Self


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    DOMAIN: str = "localhost"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    DB_HOST: Optional[str] = None
    DB_PORT: int = 5432
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_NAME: Optional[str] = None

    # PgAdmin configurations
    PGADMIN_EMAIL: Optional[str] = None
    PGADMIN_PASSWORD: Optional[str] = None

    # Security configurations
    SECRET_KEY: Optional[str] = None
    ALGORITHM: Optional[str] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = None

    # AWS configurations
    AWS_BUCKET_NAME: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_DEFAULT_REGION: Optional[str] = None

    LITERAL_API_KEY: Optional[str] = None

    # User registration details
    USER_EMAIL: Optional[str] = (
        "initial@example.com"  # Placeholder, user should replace with actual email
    )
    USER_PASSWORD: Optional[str] = (
        "your_password_here"  # Placeholder, encourage secure password handling
    )
    USER_NAME: Optional[str] = (
        "Initial User"  # Placeholder, user should replace with their actual name
    )
    USER_PROJECT_ID: Optional[str] = "PROJECT_ID_HERE"
    USER_IMAGE_PATH: Optional[str] = (
        "/path/to/image.jpg"  # Placeholder, user should replace with the path to their image
    )

    @computed_field  # type: ignore[misc]
    @property
    def DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "qS1YEUHiwNOzndTyFDH3tBPRaircbjdo":
            message = (
                f'The value of {var_name} is "qS1YEUHiwNOzndTyFDH3tBPRaircbjdo", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("DB_PASSWORD", self.DB_PASSWORD)
        self._check_default_secret("PGADMIN_PASSWORD", self.PGADMIN_PASSWORD)
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("AWS_SECRET_ACCESS_KEY", self.AWS_SECRET_ACCESS_KEY)

        return self


settings = Settings()
