import datetime
from typing import Any

from app.model.roadmap import RoadmapKey, Roadmap
from app.repository.cooud_firestore.model import ModelName
from app.repository.roadmap import IRoadmapRepository, CreateRoadmap, UpdateRoadmap


class RoadmapRepository(IRoadmapRepository):
    # Firestore Client には型が存在しないので仕方なく
    db: Any

    def __init__(self, db):
        self.db = db

    def create(self, arg: CreateRoadmap) -> [str, None]:
        doc_ref = self.db.collection(ModelName.roadmaps).document()
        roadmap = doc_ref.set({
            RoadmapKey.id: doc_ref.id,
            RoadmapKey.author_id: arg.author_id,
            RoadmapKey.title: arg.title,
            RoadmapKey.tags: arg.tags,
            RoadmapKey.favorite_count: 0,
            RoadmapKey.created_at: datetime.datetime.now(),
            RoadmapKey.updated_at: datetime.datetime.now()
        })

        if roadmap is None:
            return None

        return doc_ref.id

    def get_by_id(self, roadmap_id: str) -> Roadmap:
        doc_ref = self.db.collection(ModelName.roadmaps).document(roadmap_id)

        return Roadmap.from_dict({
            **doc_ref.get().to_dict(),
            # TODO(k-shir0): 別で取得して追加
            RoadmapKey.favorited: False,
            RoadmapKey.edges: [],
            RoadmapKey.vertexes: [],
        })

    def update(self, arg: UpdateRoadmap) -> bool:
        doc_ref = self.db.collection(ModelName.roadmaps).document(arg.id)

        # None:
        # dict を作成し None の項目があるなら削除
        # None の項目で上書きしてしまうとデータベース上で Null になってしまう
        new_dic = {k: v for k, v in arg.dict().items() if v is not None}

        success = doc_ref.update(new_dic)

        return success is not None
