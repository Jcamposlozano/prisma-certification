from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "esic-service"
    APP_ENV: str = "dev"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_DEBUG: bool = True

    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_DEFAULT_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str | None = None
    S3_SIGNATURE_BUCKET_NAME: str | None = None
    SIGNATURE_TEMPLATE_PREFIX: str = "westfield"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()