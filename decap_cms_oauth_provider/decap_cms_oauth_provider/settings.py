from os import environ
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env():
    parent = Path(__file__).resolve().parent.parent.parent
    env_file = Path.joinpath(parent, environ.get("DOTENV", ".env"))
    return env_file


class Settings(BaseSettings):
    OAUTH_CLIENT_ID: str
    OAUTH_CLIENT_SECRET: str
    GIT_HOSTNAME: str = "https://github.com"
    OAUTH_TOKEN_PATH: str = "/login/oauth/access_token"
    OAUTH_AUTHORIZE_PATH: str = "/login/oauth/authorize"
    SCOPES: str = "repo,user"

    model_config = SettingsConfigDict(extra="ignore", env_file=get_env())


settings = Settings()
