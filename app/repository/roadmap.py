import abc

from pydantic import BaseModel
from typing import List, Union

from app.model.edge import Edge
from app.model.roadmap import Roadmap, RoadmapKey
from app.model.vertex import Vertex, BaseVertex


class CreateRoadmap(BaseModel):
    author_id: str
    title: str
    tags: list
    edges: List[Edge]
    vertexes: List[BaseVertex]


class GetAllRoadmap(BaseModel):
    sorted_by: Union[RoadmapKey, None]


class UpdateRoadmap(BaseModel):
    id: str
    title: Union[str, None]
    tags: Union[list, None]


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
