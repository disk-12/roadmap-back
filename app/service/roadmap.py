from typing import Union, List

from pydantic import BaseModel

from app.model.edge import Edge
from app.model.roadmap import RoadmapKey, Roadmap
from app.model.vertex import Vertex
from app.repository.graph import IGraphRepository, UpdateGraph, CreateGraph
from app.repository.roadmap import IRoadmapRepository, CreateRoadmap, UpdateRoadmap, GetAllRoadmap
from app.repository.user_favorite import IUserFavoriteRepository


class CreateRoadmapCommand(BaseModel):
    author_id: str
    title: str
    tags: list
    edges: list
    vertexes: list


class GetRoadmapById(BaseModel):
    user_id: Union[str, None] = None
    roadmap_id: str


class UpdateRoadmapCommand(BaseModel):
    id: str
    title: Union[str, None]
    tags: Union[list, None]
    edges: Union[List[Edge], None]
    vertexes: Union[List[Vertex], None]


class RoadmapService:
    roadmap_repo: IRoadmapRepository
    graph_repo: IGraphRepository
    user_favorites_repo: IUserFavoriteRepository

    def __init__(self, roadmap_repo: IRoadmapRepository, graph_repo: IGraphRepository,
                 user_favorite_repo: IUserFavoriteRepository):
        self.roadmap_repo = roadmap_repo
        self.graph_repo = graph_repo
        self.user_favorites_repo = user_favorite_repo

    def create(self, command: CreateRoadmapCommand):
        roadmap_id = self.roadmap_repo.create(CreateRoadmap(
            author_id=command.author_id,
            title=command.title,
            tags=command.tags,
            edges=command.edges,
            vertexes=command.vertexes,
        ))

        if roadmap_id is None:
            return

        self.graph_repo.create(CreateGraph(
            id=roadmap_id,
            **command.dict()
        ))

    def get_by_id(self, command: GetRoadmapById):
        roadmap = self.roadmap_repo.get_by_id(command.roadmap_id)
        graph = self.graph_repo.get_by_id(command.roadmap_id)
        # TODO(k-shir0): ユーザから Favorite を取得し上書きする処理

        roadmap_graph = Roadmap.from_dict({
            **roadmap.dict(),
            RoadmapKey.vertexes: graph.vertexes,
            RoadmapKey.edges: graph.edges,
        })

        return roadmap_graph

    def update(self, command: UpdateRoadmapCommand) -> bool:
        roadmap_result = self.roadmap_repo.update(arg=UpdateRoadmap(**command.dict()))
        graph_result = self.graph_repo.update(arg=UpdateGraph(**command.dict()))

        return roadmap_result is not None and graph_result is not None

    def get_roadmaps_by_newest(self):
        return self.roadmap_repo.get_all(GetAllRoadmap(sorted_by=RoadmapKey.created_at))
