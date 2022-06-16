import abc

from pydantic import BaseModel
from typing import List

from app.model.edge import Edge
from app.model.roadmap import Roadmap
from app.model.vertex import Vertex


class CreateRoadmap(BaseModel):
    author_id: str
    title: str
    tags: list
    edges: List[Edge]
    vertexes: List[Vertex]


class IRoadmapRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, arg: CreateRoadmap) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(self, roadmap_id: str) -> Roadmap:
        raise NotImplementedError()