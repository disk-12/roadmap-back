import abc
from typing import List

from app.model.task import Task, CreateTask


class ITaskRepository(abc.ABC):
    @abc.abstractmethod
    def get_all(self) -> List[Task]:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, arg: CreateTask) -> bool:
        raise NotImplementedError()
