from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    allow_origins: List[str] = ["http://localhost:3000"]
    service_key: str = "/usr/src/app/serviceAccountKey.json"
    dummy_uid: str = ""

    class Config:
        env_file = ".env"
