import datetime
from typing import Any, List, Union

from google.cloud import firestore

from app.model.roadmap import RoadmapKey, Roadmap
from app.repository.cooud_firestore.model import ModelName
from app.repository.roadmap import IRoadmapRepository, CreateRoadmap, UpdateRoadmap, GetAllRoadmap, \
    UpdateRoadmapFavoriteCount


class RoadmapRepository(IRoadmapRepository):
    # Firestore Client には型が存在しないので仕方なく
    db: Any

    def __init__(self, db):
        self.db = db

    def create(self, arg: CreateRoadmap) -> Union[str, None]:
        doc_ref = self.db.collection(ModelName.roadmaps).document()
        roadmap = doc_ref.set({
            RoadmapKey.id: doc_ref.id,
            RoadmapKey.author_id: arg.author_id,
            RoadmapKey.title: arg.title,
            RoadmapKey.tags: arg.tags,
            RoadmapKey.locked: arg.locked,
            RoadmapKey.thumbnail: arg.thumbnail,
            RoadmapKey.favorite_count: 0,
            RoadmapKey.created_at: datetime.datetime.now(),
            RoadmapKey.updated_at: datetime.datetime.now()
        })

        if roadmap is None:
            return None

        return doc_ref.id

    def get_all(self, arg: GetAllRoadmap) -> List[Roadmap]:
        query = self.db.collection(ModelName.roadmaps)

        if arg.sorted_by is not None:
            query = query.order_by(arg.sorted_by.value)

        if arg.id_filter is not None:
            if len(arg.id_filter) > 10:
                raise ValueError("id_filter は 10 以下である必要があります")

            query = query.where(RoadmapKey.id, "in", arg.id_filter)

        if arg.author_id is not None:
            query = query.where(RoadmapKey.author_id, "==", arg.author_id)

        docs = query.get()

        ary = []
        for doc in docs:
            ary.append(self.dict_to_roadmap(doc.to_dict()))

        return ary

    def get_by_id(self, roadmap_id: str) -> Roadmap:
        doc_ref = self.db.collection(ModelName.roadmaps).document(roadmap_id)

        return self.dict_to_roadmap(doc_ref.get().to_dict())

    def update(self, arg: UpdateRoadmap) -> bool:
        doc_ref = self.db.collection(ModelName.roadmaps).document(arg.id)

        # None:
        # dict を作成し None の項目があるなら削除
        # None の項目で上書きしてしまうとデータベース上で Null になってしまう
        new_dic = {k: v for k, v in arg.dict().items() if v is not None}

        success = doc_ref.update(new_dic)

        return success is not None

    @staticmethod
    def dict_to_roadmap(roadmap_dict: dict) -> Roadmap:
        return Roadmap(
            **roadmap_dict,
            favorited=False,
            edges=[],
            vertexes=[],
            achievement=None,
        )

    def update_favorite_count(self, arg: UpdateRoadmapFavoriteCount) -> bool:
        doc_ref = self.db.collection(ModelName.roadmaps).document(arg.id)

        success = doc_ref.update({RoadmapKey.favorite_count: firestore.Increment(arg.count)})

        return success is not None
