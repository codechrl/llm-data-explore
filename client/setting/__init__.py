import os

from pydantic import BaseSettings


class Setting(BaseSettings):
    API_ENDPOINT: str

    class Config:
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
            API_ENDPOINT=os.environ.get("API_ENDPOINT", ""),
        )
    return setting


setting = load_settings()
