from pydantic import BaseModel

from app.repository.roadmap import IRoadmapRepository, UpdateRoadmapFavoriteCount
from app.repository.user_favorite import IUserFavoriteRepository, AddRoadmapId, DeleteRoadmapId, FindByUserId


class AddFavoriteCommand(BaseModel):
    user_id: str
    roadmap_id: str


class DeleteFavoriteCommand(BaseModel):
    user_id: str
    roadmap_id: str


class UserFavoriteService:
    user_favorite_repo: IUserFavoriteRepository
    roadmap_repo: IRoadmapRepository

    def __init__(self, user_favorite_repo: IUserFavoriteRepository, roadmap_repo: IRoadmapRepository):
        self.user_favorite_repo = user_favorite_repo
        self.roadmap_repo = roadmap_repo

    def add_favorite(self, command: AddFavoriteCommand) -> bool:
        exist = self.exist_favorite(user_id=command.user_id, roadmap_id=command.roadmap_id)
        if exist:
            return False

        result = self.user_favorite_repo.add_roadmap_id(AddRoadmapId(
            user_id=command.user_id,
            roadmap_id=command.roadmap_id,
        ))

        self.roadmap_repo.update_favorite_count(
            UpdateRoadmapFavoriteCount(id=command.roadmap_id, count=1)
        )

        return True

    def delete_favorite(self, command: DeleteFavoriteCommand) -> bool:
        exist = self.exist_favorite(user_id=command.user_id, roadmap_id=command.roadmap_id)
        if not exist:
            return False

        self.user_favorite_repo.remove_roadmap_id(DeleteRoadmapId(
            user_id=command.user_id,
            roadmap_id=command.roadmap_id,
        ))

        self.roadmap_repo.update_favorite_count(
            UpdateRoadmapFavoriteCount(id=command.roadmap_id, count=-1)
        )

        return True

    def exist_favorite(self, user_id: str, roadmap_id: str) -> bool:
        favorite = self.user_favorite_repo.get_by_user_id(FindByUserId(id=user_id))
        return roadmap_id in favorite.roadmap_ids
