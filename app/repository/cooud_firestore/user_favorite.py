from typing import Any, Union

from google.cloud import firestore

from app.model.user_favorite import UserFavorite, UserFavoriteKey
from app.repository.cooud_firestore.model import ModelName
from app.repository.user_favorite import IUserFavoriteRepository, FindByUserId, AddRoadmapId, DeleteRoadmapId


class UserFavoriteRepository(IUserFavoriteRepository):
    # Firestore Client には型が存在しないので仕方なく
    db: Any

    def __init__(self, db):
        self.db = db

    def get_by_user_id(self, arg: FindByUserId) -> Union[UserFavorite, None]:
        docs = self.db.collection(ModelName.user_favorites).document(arg.id).get()

        if not docs.exists:
            return None

        return UserFavorite.from_dict(docs.to_dict())

    def add_roadmap_id(self, arg: AddRoadmapId) -> bool:
        favorite = self.get_by_user_id(FindByUserId(id=arg.user_id))

        doc_ref = self.db.collection(ModelName.user_favorites).document(arg.user_id)

        if favorite is None:
            doc_ref.set({
                UserFavoriteKey.id: arg.user_id,
                UserFavoriteKey.roadmap_ids: [],
            })

            # TODO(k-shir0): 作成できなかったら エラー処理

        success = doc_ref.update({
            UserFavoriteKey.roadmap_ids: firestore.ArrayUnion([arg.roadmap_id])
        })

        # TODO(k-shir0): 追加出来なかったら エラー処理

        return success is not None

    def remove_roadmap_id(self, arg: DeleteRoadmapId) -> bool:
        doc_ref = self.db.collection(ModelName.user_favorites).document(arg.user_id)

        success = doc_ref.update({
            UserFavoriteKey.roadmap_ids: firestore.ArrayRemove([arg.roadmap_id])
        })

        return success is not None
