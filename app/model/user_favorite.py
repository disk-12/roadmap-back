from enum import Enum
from typing import List

from pydantic import BaseModel


class UserFavoriteKey(str, Enum):
    id = u"id"
    roadmap_ids = u"roadmap_ids"


class UserFavorite(BaseModel):
    id: str
    roadmap_ids: List[str]

    @staticmethod
    def from_dict(source: dict):
        return UserFavorite(
            id=source[UserFavoriteKey.id],
            roadmap_ids=source[UserFavoriteKey.roadmap_ids]
        )
