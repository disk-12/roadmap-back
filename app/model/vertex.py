import datetime
from enum import Enum

from pydantic import BaseModel


class VertexKey(str, Enum):
    id = u"id"
    x_coordinate = u"x_coordinate"
    y_coordinate = u"y_coordinate"


class Vertex(BaseModel):
    id: str
    x_coordinate: int
    y_coordinate: int

    @staticmethod
    def from_dict(source):
        return Vertex(
            id=source[VertexKey.id],
            x_coordinate=source[VertexKey.x_coordinate],
            y_coordinate=source[VertexKey.y_coordinate]
        )
