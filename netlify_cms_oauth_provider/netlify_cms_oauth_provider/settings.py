from os import environ
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    OAUTH_CLIENT_ID: str
    OAUTH_CLIENT_SECRET: str
    GIT_HOSTNAME: str = "https://github.com"
    OAUTH_TOKEN_PATH: str = "/login/oauth/access_token"
    OAUTH_AUTHORIZE_PATH: str = "/login/oauth/authorize"
    SCOPES: str = "repo,user"

    class Config:
        parent = Path(__file__).resolve().parent.parent.parent
        if "DOTENV" in environ:
            env_file = Path.joinpath(parent, environ["DOTENV"])
        else:
            env_file = Path.joinpath(parent, ".env")


settings = Settings()
