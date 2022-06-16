import abc

from pydantic import BaseModel


class CreateRoadmap(BaseModel):
    author_id: str
    title: str
    tags: list
    edges: list
    vertexes: list


class IRoadmapRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, arg: CreateRoadmap) -> bool:
        raise NotImplementedError()
