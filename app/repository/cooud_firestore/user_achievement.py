from typing import Union, Any

from app.model.user_achievement import UserAchievement, UserAchievementKey
from app.repository.cooud_firestore.model import ModelName
from app.repository.user_achievement import IUserAchievementRepository, FindUserAchievementByRoadmapId, \
    UpdateUserAchievement


class UserAchievementRepository(IUserAchievementRepository):
    # Firestore Client には型が存在しないので仕方なく
    db: Any

    def __init__(self, db):
        self.db = db

    def get_by_roadmap_id(self, arg: FindUserAchievementByRoadmapId) -> Union[UserAchievement, None]:
        result = self.db \
            .collection(ModelName.user_achievement) \
            .document(arg.user_id).collection(ModelName.roadmaps) \
            .document(arg.roadmap_id).get()

        achievement_dict = result.to_dict()

        if achievement_dict is None:
            return None

        return UserAchievement.from_dict(achievement_dict)

    def update_user_achievement(self, arg: UpdateUserAchievement) -> bool:
        doc_ref = self.db \
            .collection(ModelName.user_achievement) \
            .document(arg.user_id).collection(ModelName.roadmaps) \
            .document(arg.roadmap_id)

        result = doc_ref.set({
            UserAchievementKey.roadmap_id: arg.roadmap_id,
            UserAchievementKey.rate: arg.rate,
            UserAchievementKey.vertex_ids: arg.vertex_ids
        })

        return result is not None
