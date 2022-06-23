from typing import Union, List

from pydantic import BaseModel

from app.model.edge import Edge
from app.model.roadmap import RoadmapKey, Roadmap
from app.model.user_achievement import UserAchievement
from app.model.vertex import Vertex, VertexKey, BaseVertex, BaseYoutubeVertex, BaseLinkVertex
from app.repository.graph import IGraphRepository, UpdateGraph, CreateGraph
from app.repository.roadmap import IRoadmapRepository, CreateRoadmap, UpdateRoadmap, GetAllRoadmap
from app.repository.roadmap_search import IRoadmapSearchRepository, SearchRoadmap
from app.repository.user_achievement import IUserAchievementRepository, FindAllUserAchievements, \
    FindUserAchievementByRoadmapId
from app.repository.user_favorite import IUserFavoriteRepository, FindByUserId


class CreateRoadmapCommand(BaseModel):
    author_id: str
    title: str
    tags: List[str]
    edges: List[Edge]
    vertexes: List[Union[BaseVertex, BaseYoutubeVertex, BaseLinkVertex]]
    thumbnail: Union[str, None]


class GetRoadmapById(BaseModel):
    user_id: Union[str, None] = None
    roadmap_id: str


class UpdateRoadmapCommand(BaseModel):
    id: str
    title: Union[str, None]
    tags: Union[list, None]
    edges: Union[List[Edge], None]
    vertexes: Union[List[Union[BaseVertex, BaseYoutubeVertex, BaseLinkVertex]], None]
    thumbnail: Union[str, None]


class GetRoadmapsByNewestCommand(BaseModel):
    user_id: Union[str, None]


class SearchRoadmapsCommand(BaseModel):
    keyword: str
    user_id: Union[str, None]


class RoadmapService:
    roadmap_repo: IRoadmapRepository
    graph_repo: IGraphRepository
    user_favorites_repo: IUserFavoriteRepository
    user_achievement_repo: IUserAchievementRepository
    roadmap_search_repo: IRoadmapSearchRepository

    def __init__(self, roadmap_repo: IRoadmapRepository, graph_repo: IGraphRepository,
                 user_favorite_repo: IUserFavoriteRepository, user_achievement_repo: IUserAchievementRepository,
                 roadmap_search_repo: IRoadmapSearchRepository):
        self.roadmap_repo = roadmap_repo
        self.graph_repo = graph_repo
        self.user_favorites_repo = user_favorite_repo
        self.user_achievement_repo = user_achievement_repo
        self.roadmap_search_repo = roadmap_search_repo

    def create(self, command: CreateRoadmapCommand):
        roadmap_id = self.roadmap_repo.create(CreateRoadmap(
            author_id=command.author_id,
            title=command.title,
            tags=command.tags,
            thumbnail=command.thumbnail,
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
        favorite = False
        achievement = None
        vertexes = graph.vertexes

        # ユーザお気に入り一覧と実績一覧を取得
        if command.user_id is not None:
            # お気に入り一覧
            user_favorite = self.user_favorites_repo.get_by_user_id(FindByUserId(id=command.user_id))
            if user_favorite is not None:
                favorite = command.roadmap_id in user_favorite.roadmap_ids

            # 実績一覧
            achievement = self.user_achievement_repo.get_by_roadmap_id(
                FindUserAchievementByRoadmapId(roadmap_id=roadmap.id, user_id=command.user_id))

            if achievement is not None:
                # 各 Vertex に Achieved かセットする
                new_vertexes = []
                for vertex in vertexes:
                    achieved = vertex.id in achievement.vertex_ids
                    new_vertexes.append(Vertex(**vertex.dict(), achieved=achieved))
                vertexes = new_vertexes

        roadmap_graph = Roadmap.from_dict({
            **roadmap.dict(),
            RoadmapKey.favorited: favorite,
            RoadmapKey.vertexes: vertexes,
            RoadmapKey.edges: graph.edges,
            RoadmapKey.achievement: achievement,
        })

        return roadmap_graph

    def update(self, command: UpdateRoadmapCommand) -> bool:
        roadmap_result = self.roadmap_repo.update(arg=UpdateRoadmap(**command.dict()))
        graph_result = self.graph_repo.update(arg=UpdateGraph(**command.dict()))

        return roadmap_result is not None and graph_result is not None

    def get_roadmaps_by_newest(self, command: GetRoadmapsByNewestCommand):
        roadmaps = self.roadmap_repo.get_all(GetAllRoadmap(sorted_by=RoadmapKey.created_at))

        return self.with_roadmaps(user_id=command.user_id, roadmaps=roadmaps)

    def search_roadmaps(self, command: SearchRoadmapsCommand) -> List[Roadmap]:
        roadmaps = self.roadmap_search_repo.search(SearchRoadmap(keyword=command.keyword))

        # algolia から取得された物はソートされていないため、ソートする
        sorted_roadmaps = sorted(roadmaps, key=lambda roadmap: roadmap.created_at, reverse=True)

        return self.with_roadmaps(user_id=command.user_id, roadmaps=sorted_roadmaps)

    # 各ロードマップお気に入りと実績を追加
    def with_roadmaps(self, user_id: str, roadmaps: List[Roadmap]) -> List[Roadmap]:
        # ユーザお気に入り一覧と実績一覧を取得
        favorite_roadmap_ids: List[str] = []
        user_achievements: List[UserAchievement] = []
        if user_id is not None:
            # お気に入り一覧
            user_favorite = self.user_favorites_repo.get_by_user_id(FindByUserId(id=user_id))
            if user_favorite is not None:
                favorite_roadmap_ids = user_favorite.roadmap_ids

            # 実績一覧
            user_achievements = self.user_achievement_repo.get_all_roadmap(
                FindAllUserAchievements(user_id=user_id))

        new_roadmaps: List[Roadmap] = []
        for roadmap in roadmaps:
            favorite = roadmap.id in favorite_roadmap_ids
            achievement = next((x for x in user_achievements if x.roadmap_id == roadmap.id), None)

            new_roadmaps.append(Roadmap.from_dict({
                **roadmap.dict(),
                RoadmapKey.favorited: favorite,
                RoadmapKey.achievement: achievement,
            }))

        return new_roadmaps
