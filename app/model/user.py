import datetime
from enum import Enum

from pydantic import BaseModel


class UserKey(str, Enum):
    id = u'id'
    name = u'name'
    last_login_at = u'last_login_at'
    created_at = u'created_at'
    updated_at = u'updated_at'


class User(BaseModel):
    id: str
    name: str
    last_login_at: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @staticmethod
    def from_dict(source):
        return User(
            id=source[UserKey.id],
            name=source[UserKey.name],
            last_login_at=source[UserKey.updated_at],
            created_at=source[UserKey.created_at],
            updated_at=source[UserKey.updated_at]
        )
