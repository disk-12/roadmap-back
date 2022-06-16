import abc
import datetime
from typing import Union

from pydantic import BaseModel

from app.model.user import User


class FindUser(BaseModel):
    id: str


class CreateUser(BaseModel):
    id: str
    name: str


class UpdateUser(BaseModel):
    id: str
    name: Union[str, None] = None
    last_login_at: Union[datetime.datetime, None] = None


class IUserRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, arg: FindUser) -> [User, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, arg: CreateUser) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, arg: UpdateUser) -> bool:
        raise NotImplementedError()
