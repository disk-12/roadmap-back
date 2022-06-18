import abc
from typing import Union

from pydantic import BaseModel

from app.model.user_favorite import UserFavorite


class FindByUserId(BaseModel):
    id: str


class AddRoadmapId(BaseModel):
    user_id: str
    roadmap_id: str


class DeleteRoadmapId(BaseModel):
    user_id: str
    roadmap_id: str


class IUserFavoriteRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_user_id(self, arg: FindByUserId) -> Union[UserFavorite, None]:
        raise NotImplementedError()

    @abc.abstractmethod
    def add_roadmap_id(self, arg: AddRoadmapId) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def remove_roadmap_id(self, arg: DeleteRoadmapId) -> bool:
        raise NotImplementedError()
