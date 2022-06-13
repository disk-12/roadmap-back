from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    allow_origins: List[str] = ["https://localhost:3000"]
    service_key: str = "/usr/src/app/serviceAccountKey.json"

    class Config:
        env_file = ".env"
