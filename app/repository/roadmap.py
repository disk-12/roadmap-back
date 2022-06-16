import abc

from pydantic import BaseModel
from typing import List, Union

from app.model.edge import Edge
from app.model.roadmap import Roadmap
from app.model.vertex import Vertex


class CreateRoadmap(BaseModel):
    author_id: str
    title: str
    tags: list
    edges: List[Edge]
    vertexes: List[Vertex]


class UpdateRoadmap(BaseModel):
    id: str
    title: Union[str, None]
    tags: Union[list, None]


class IRoadmapRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, arg: CreateRoadmap) -> Union[str, None]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(self, roadmap_id: str) -> Roadmap:
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, arg: UpdateRoadmap) -> bool:
        raise NotImplementedError()
