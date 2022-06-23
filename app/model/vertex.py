from enum import Enum
from typing import Union, Literal

from pydantic import BaseModel


class VertexKey(str, Enum):
    id = u"id"
    type = u"type"
    x_coordinate = u"x_coordinate"
    y_coordinate = u"y_coordinate"
    title = u"title"
    content = u"content"
    achieved = u"achieved"

    youtube_id = u"youtube_id"
    youtube_start = u"youtube_start"
    youtube_end = u"youtube_end"

    link = u"link"
    ogp_url = u"ogp_url"
    ogp_title = u"ogp_title"
    ogp_description = u"ogp_description"
    ogp_site_name = u"ogp_site_name"
    ogp_image = u"ogp_image"


class VertexType(str, Enum):
    default = u"DEFAULT"
    youtube = u"YOUTUBE"
    link = u"LINK"


class BaseVertex(BaseModel):
    id: str
    type: Literal[VertexType.default]
    x_coordinate: int
    y_coordinate: int
    title: str
    content: str


class Vertex(BaseVertex):
    achieved: bool

    @staticmethod
    def from_dict(source):
        return Vertex(
            id=source[VertexKey.id],
            type=source[VertexKey.type],
            x_coordinate=source[VertexKey.x_coordinate],
            y_coordinate=source[VertexKey.y_coordinate],
            title=source[VertexKey.title],
            content=source[VertexKey.content],
            achieved=source[VertexKey.achieved],
        )


class BaseYoutubeVertex(BaseVertex):
    type: Literal[VertexType.youtube]
    youtube_id: str
    youtube_start: Union[int, None]
    youtube_end: Union[int, None]


class YoutubeVertex(Vertex, BaseYoutubeVertex):
    @staticmethod
    def from_dict(source: dict):
        return YoutubeVertex(
            id=source[VertexKey.id],
            type=source[VertexKey.type],
            x_coordinate=source[VertexKey.x_coordinate],
            y_coordinate=source[VertexKey.y_coordinate],
            title=source[VertexKey.title],
            content=source[VertexKey.content],
            achieved=source[VertexKey.achieved],
            youtube_id=source[VertexKey.youtube_id],
            youtube_start=source[VertexKey.youtube_start],
            youtube_end=source[VertexKey.youtube_end],
        )


class BaseLinkVertex(BaseVertex):
    type: Literal[VertexType.link]
    link: str


# NOTE:
# Firestore に入れるためだけの型
class InLinkVertex(BaseLinkVertex):
    ogp_url: Union[str, None]
    ogp_title: Union[str, None]
    ogp_description: Union[str, None]
    ogp_site_name: Union[str, None]
    ogp_image: Union[str, None]

    @staticmethod
    def from_dict(source: dict):
        return InLinkVertex(
            id=source[VertexKey.id],
            type=source[VertexKey.type],
            x_coordinate=source[VertexKey.x_coordinate],
            y_coordinate=source[VertexKey.y_coordinate],
            title=source[VertexKey.title],
            content=source[VertexKey.content],
            link=source[VertexKey.link],
            ogp_url=source[VertexKey.ogp_url],
            ogp_title=source[VertexKey.ogp_title],
            ogp_description=source[VertexKey.ogp_description],
            ogp_site_name=source[VertexKey.ogp_site_name],
            ogp_image=source[VertexKey.ogp_image],
        )


class LinkVertex(Vertex, BaseLinkVertex):
    ogp_url: Union[str, None]
    ogp_title: Union[str, None]
    ogp_description: Union[str, None]
    ogp_site_name: Union[str, None]
    ogp_image: Union[str, None]

    @staticmethod
    def from_dict(source: dict):
        return LinkVertex(
            id=source[VertexKey.id],
            type=source[VertexKey.type],
            x_coordinate=source[VertexKey.x_coordinate],
            y_coordinate=source[VertexKey.y_coordinate],
            title=source[VertexKey.title],
            content=source[VertexKey.content],
            achieved=source[VertexKey.achieved],
            link=source[VertexKey.link],
            ogp_url=source[VertexKey.ogp_url],
            ogp_title=source[VertexKey.ogp_title],
            ogp_description=source[VertexKey.ogp_description],
            ogp_site_name=source[VertexKey.ogp_site_name],
            ogp_image=source[VertexKey.ogp_image],
        )
