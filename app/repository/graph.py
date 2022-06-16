import abc
import datetime
from typing import Union, List

from pydantic import BaseModel

from app.model.edge import Edge
from app.model.graph import Graph
from app.model.vertex import Vertex


class CreateGraph(BaseModel):
    id: str
    edges: List[Edge]
    vertexes: List[Vertex]


class UpdateGraph(BaseModel):
    id: str
    edges: Union[List[Edge], None]
    vertexes: Union[List[Vertex], None]
    updated_at: Union[datetime.datetime, None]


class IGraphRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, arg: CreateGraph) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(self, roadmap_id: str) -> Graph:
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, arg: UpdateGraph) -> bool:
        raise NotImplementedError()
