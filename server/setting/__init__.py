import os

from pydantic import BaseSettings


class Setting(BaseSettings):
    DBSTRING: str
    OPENAI_API_KEY: str
    FASTAPI_SECRET_KEY: str
    GITHUB_USER: str
    GIHUB_PAT: str
    PUBLIC_HOSTNAME: str

    class Config:
        # Calculate the path to the .env.dev file two directories above the current script
        env_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..", ".env.dev")
        )
        case_sensitive = True


def load_settings():
    try:
        setting = Setting()
    except Exception as e:
        print(f"Error loading settings from env_file: {e}, getting env from os environ")
        setting = Setting(
            DBSTRING=os.environ.get("DBSTRING", ""),
            OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY", ""),
            FASTAPI_SECRET_KEY=os.environ.get("FASTAPI_SECRET_KEY", ""),
            GITHUB_USER=os.environ.get("GITHUB_USER", ""),
            GIHUB_PAT=os.environ.get("GIHUB_PAT", ""),
            PUBLIC_HOSTNAME=os.environ.get("PUBLIC_HOSTNAME", ""),
        )
    return setting


setting = load_settings()
