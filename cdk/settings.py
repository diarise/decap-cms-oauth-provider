from os import environ
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT: str = None
    PRODUCT: str = None
    ENV: str = "staging"
    LOG_LEVEL: str = "INFO"
    HOSTED_ZONE_ID: str = None
    HOSTED_ZONE_NAME: str = None
    DOMAIN_NAME: str = None
    CORS_ALLOW_ORIGIN: str = "*"
    CERTIFICATE_ARN: str = None
    API_LAMBDA_MEMORY_SIZE: int = 128
    API_LAMBDA_TIMEOUT: int = 10  # lambda timeout in seconds

    class Config:
        parent = Path(__file__).resolve().parent.parent
        if "DOTENV" in environ:
            env_file = Path.joinpath(parent, environ["DOTENV"])
        else:
            env_file = Path.joinpath(parent, ".env")


settings = Settings()
