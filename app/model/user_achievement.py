from enum import Enum
from typing import List

from pydantic import BaseModel


class UserAchievementKey(str, Enum):
    roadmap_id = u"roadmap_id"
    rate = u"rate"
    vertex_ids = u"vertex_ids"


class UserAchievement(BaseModel):
    roadmap_id: str
    rate: int
    vertex_ids: List[str]

    @staticmethod
    def from_dict(source: dict):
        return UserAchievement(
            roadmap_id=source[UserAchievementKey.roadmap_id],
            rate=source[UserAchievementKey.rate],
            vertex_ids=source[UserAchievementKey.vertex_ids],
        )
