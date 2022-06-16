from enum import Enum

from pydantic import BaseModel


class EdgeKey(str, Enum):
    id = u"id"
    source_id = u"source_id"
    target_id = u"target_id"
    is_solid_line = u"is_solid_line"


class Edge(BaseModel):
    id: str
    source_id: str
    target_id: str
    is_solid_line: bool

    @staticmethod
    def from_dict(source):
        return Edge(
            id=source[EdgeKey.id],
            source_id=source[EdgeKey.source_id],
            target_id=source[EdgeKey.target_id],
            is_solid_line=source[EdgeKey.is_solid_line]
        )
