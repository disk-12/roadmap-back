import abc

from pydantic import BaseModel

from app.model.user import User


class FindUser(BaseModel):
    id: str


class CreateUser(BaseModel):
    id: str
    name: str


class IUserRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, arg: FindUser) -> [User, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, arg: CreateUser) -> bool:
        raise NotImplementedError()
