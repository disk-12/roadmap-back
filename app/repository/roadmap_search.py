import abc
from typing import List

from pydantic import BaseModel

from app.model.roadmap import Roadmap


class SearchRoadmap(BaseModel):
    keyword: str


class IRoadmapSearchRepository(abc.ABC):
    @abc.abstractmethod
    def search(self, arg: SearchRoadmap) -> List[Roadmap]:
        raise NotImplementedError()
