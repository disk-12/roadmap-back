import datetime
from enum import Enum
from typing import List, Any, Union

from pydantic import BaseModel

from app.model.edge import Edge
from app.model.vertex import Vertex, YoutubeVertex, LinkVertex


class GraphKey(str, Enum):
    id = u'id'
    edges = u'edges'
    vertexes = u'vertexes'
    created_at = u'created_at'
    updated_at = u'updated_at'


class Graph(BaseModel):
    id: str
    edges: List[Edge]
    vertexes: List[Union[Vertex, YoutubeVertex, LinkVertex]]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @staticmethod
    def from_dict(source):
        return Graph(
            id=source[GraphKey.id],
            edges=source[GraphKey.edges],
            vertexes=source[GraphKey.vertexes],
            created_at=source[GraphKey.created_at],
            updated_at=source[GraphKey.updated_at]
        )
