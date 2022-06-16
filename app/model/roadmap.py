import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel

from app.model.edge import Edge
from app.model.vertex import Vertex


class RoadmapKey(str, Enum):
    id = u"id"
    author_id = u"author_id"
    title = u"title"
    favorited = u"favorited"
    favorite_count = u"favorite_count"
    tags = u"tags"
    edges = u"edges"
    vertexes = u"vertexes"
    created_at = u'created_at'
    updated_at = u'updated_at'


class Roadmap(BaseModel):
    id: str
    author_id: str
    title: str
    favorited: bool
    favorite_count: int
    tags: list
    edges: List[Edge]
    vertexes: List[Vertex]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @staticmethod
    def from_dict(source):
        vertexes: List[Vertex] = source[RoadmapKey.vertexes]

        return Roadmap(
            id=source[RoadmapKey.id],
            author_id=source[RoadmapKey.author_id],
            title=source[RoadmapKey.title],
            favorited=source[RoadmapKey.favorited],
            favorite_count=source[RoadmapKey.favorite_count],
            tags=source[RoadmapKey.tags],
            edges=source[RoadmapKey.edges],
            vertexes=vertexes,
            created_at=source[RoadmapKey.created_at],
            updated_at=source[RoadmapKey.updated_at]
        )
