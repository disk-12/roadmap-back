from pydantic import BaseModel

from app.repository.user_favorite import IUserFavoriteRepository, AddRoadmapId, DeleteRoadmapId


class AddFavoriteCommand(BaseModel):
    user_id: str
    roadmap_id: str


class DeleteFavoriteCommand(BaseModel):
    user_id: str
    roadmap_id: str


class UserFavoriteService:
    user_favorite_repo: IUserFavoriteRepository

    def __init__(self, user_favorite_repo: IUserFavoriteRepository):
        self.user_favorite_repo = user_favorite_repo

    def add_favorite(self, command: AddFavoriteCommand) -> bool:
        return self.user_favorite_repo.add_roadmap_id(AddRoadmapId(
            user_id=command.user_id,
            roadmap_id=command.roadmap_id,
        ))

    def delete_favorite(self, command: DeleteFavoriteCommand) -> bool:
        return self.user_favorite_repo.remove_roadmap_id(DeleteRoadmapId(
            user_id=command.user_id,
            roadmap_id=command.roadmap_id,
        ))
