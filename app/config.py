from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    allow_origins: List[str] = ["http://localhost:3000"]
    service_key: str = "/usr/src/app/serviceAccountKey.json"
    algolia_app_key: str = "YOUR_APP_KEY"
    algolia_app_id: str = "YOUR_APP_ID"
    dummy_uid: str = "YOUR_DUMMY_ID"

    class Config:
        env_file = ".env"
