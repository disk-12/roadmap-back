from enum import Enum

from pydantic import BaseModel


class VertexKey(str, Enum):
    id = u"id"
    x_coordinate = u"x_coordinate"
    y_coordinate = u"y_coordinate"
    achieved = u"achieved"


class BaseVertex(BaseModel):
    id: str
    x_coordinate: int
    y_coordinate: int


class Vertex(BaseVertex):
    achieved: bool

    @staticmethod
    def from_dict(source):
        return Vertex(
            id=source[VertexKey.id],
            x_coordinate=source[VertexKey.x_coordinate],
            y_coordinate=source[VertexKey.y_coordinate],
            achieved=source[VertexKey.achieved],
        )
