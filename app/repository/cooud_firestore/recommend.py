from typing import Any

from app.model.reccomend import Recommend
from app.repository.cooud_firestore.model import ModelName
from app.repository.recommend import IRecommendRepository


class RecommendRepository(IRecommendRepository):
    # Firestore Client には型が存在しないので仕方なく
    db: Any

    def __init__(self, db):
        self.db = db

    def get_recommends(self) -> Recommend:
        recommend = self.db.collection(ModelName.recommends).document("roadmap_ids").get()
        return Recommend(**recommend.to_dict())
