import abc
from typing import Union, List

from pydantic import BaseModel

from app.model.user_achievement import UserAchievement


class FindUserAchievementByRoadmapId(BaseModel):
    user_id: str
    roadmap_id: str


class UpdateUserAchievement(BaseModel):
    user_id: str
    roadmap_id: str
    rate: int
    vertex_ids: List[str]


class FindAllUserAchievements(BaseModel):
    user_id: str


class IUserAchievementRepository(abc.ABC):
    @abc.abstractmethod
    def get_all_roadmap(self, arg: FindAllUserAchievements) -> List[UserAchievement]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_roadmap_id(self, arg: FindUserAchievementByRoadmapId) -> Union[UserAchievement, None]:
        raise NotImplementedError()

    @abc.abstractmethod
    def update_user_achievement(self, arg: UpdateUserAchievement) -> bool:
        raise NotImplementedError()
