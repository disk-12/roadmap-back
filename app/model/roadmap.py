import datetime
from enum import Enum
from typing import List, Union

from pydantic import BaseModel

from app.model.edge import Edge
from app.model.user_achievement import UserAchievement
from app.model.vertex import Vertex, LinkVertex, YoutubeVertex


class RoadmapKey(str, Enum):
    id = u"id"
    author_id = u"author_id"
    title = u"title"
    favorited = u"favorited"
    favorite_count = u"favorite_count"
    tags = u"tags"
    edges = u"edges"
    vertexes = u"vertexes"
    locked = u"locked"
    thumbnail = u"thumbnail"
    achievement = u"achievement"
    created_at = u'created_at'
    updated_at = u'updated_at'


class Roadmap(BaseModel):
    id: str
    author_id: str
    title: str
    favorited: bool
    favorite_count: int
    tags: List[str]
    edges: List[Edge]
    vertexes: List[Union[Vertex, LinkVertex, YoutubeVertex]]
    locked: bool
    thumbnail: Union[str, None]
    achievement: Union[UserAchievement, None]
    created_at: datetime.datetime
    updated_at: datetime.datetime
