import abc

from pydantic import BaseModel
from typing import List, Union

from app.model.roadmap import Roadmap, RoadmapKey


class CreateRoadmap(BaseModel):
    author_id: str
    title: str
    tags: List[str]
    locked: bool
    thumbnail: Union[str, None]


class GetAllRoadmap(BaseModel):
    sorted_by: Union[RoadmapKey, None]
    id_filter: Union[List[str], None]


class UpdateRoadmap(BaseModel):
    id: str
    title: Union[str, None]
    tags: Union[list, None]
    locked: Union[bool, None]
    thumbnail: Union[str, None]


class UpdateRoadmapFavoriteCount(BaseModel):
    id: str
    count: int


class IRoadmapRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, arg: CreateRoadmap) -> Union[str, None]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all(self, arg: GetAllRoadmap) -> List[Roadmap]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(self, roadmap_id: str) -> Roadmap:
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, arg: UpdateRoadmap) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def update_favorite_count(self, arg: UpdateRoadmapFavoriteCount) -> bool:
        raise NotImplementedError()
