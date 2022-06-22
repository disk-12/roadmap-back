import math
from typing import List, Set

from pydantic import BaseModel

from app.repository.graph import IGraphRepository
from app.repository.user_achievement import IUserAchievementRepository, UpdateUserAchievement, \
    FindUserAchievementByRoadmapId


class GiveAchievementCommand(BaseModel):
    user_id: str
    roadmap_id: str
    vertex_id: str


class TakeAchievementCommand(BaseModel):
    user_id: str
    roadmap_id: str
    vertex_id: str


class UserAchievementService:
    user_achievement_repo: IUserAchievementRepository
    graph_repo: IGraphRepository

    def __init__(self, user_achievement_repo: IUserAchievementRepository, graph_repo: IGraphRepository):
        self.user_achievement_repo = user_achievement_repo
        self.graph_repo = graph_repo

    def give_achievement(self, command: GiveAchievementCommand) -> bool:
        graph = self.graph_repo.get_by_id(roadmap_id=command.roadmap_id)

        vertex_ids: List[str] = []
        for vertex in graph.vertexes:
            vertex_ids.append(vertex.id)

        achievement = self.user_achievement_repo.get_by_roadmap_id(
            FindUserAchievementByRoadmapId(user_id=command.user_id, roadmap_id=command.roadmap_id))

        # 重複排除と値チェック
        new_vertex_ids: Set[str] = {command.vertex_id}
        if achievement is not None:
            # 既存の配列から該当IDを追加
            new_vertex_ids = {*achievement.vertex_ids, command.vertex_id}

        new_vertex_ids = new_vertex_ids & set(vertex_ids)

        return self.user_achievement_repo.update_user_achievement(
            UpdateUserAchievement(
                user_id=command.user_id,
                roadmap_id=command.roadmap_id,
                rate=math.floor(len(new_vertex_ids) / len(vertex_ids) * 100),
                vertex_ids=list(new_vertex_ids),
            )
        )

    def take_achievement(self, command: TakeAchievementCommand):
        graph = self.graph_repo.get_by_id(roadmap_id=command.roadmap_id)

        vertex_ids: List[str] = []
        for vertex in graph.vertexes:
            vertex_ids.append(vertex.id)

        achievement = self.user_achievement_repo.get_by_roadmap_id(
            FindUserAchievementByRoadmapId(user_id=command.user_id, roadmap_id=command.roadmap_id))

        # 重複排除と値チェック
        new_vertex_ids: Set[str] = set([])
        if achievement is not None:
            # 既存の配列から該当IDを削除
            new_vertex_ids = set(achievement.vertex_ids)
            new_vertex_ids.remove(command.vertex_id)

        new_vertex_ids = new_vertex_ids & set(vertex_ids)

        return self.user_achievement_repo.update_user_achievement(
            UpdateUserAchievement(
                user_id=command.user_id,
                roadmap_id=command.roadmap_id,
                rate=math.floor(len(new_vertex_ids) / len(vertex_ids) * 100),
                vertex_ids=list(new_vertex_ids),
            )
        )
