import datetime
from typing import Any

from app.model.roadmap import RoadmapKey
from app.repository.cooud_firestore.model import ModelName
from app.repository.roadmap import IRoadmapRepository, CreateRoadmap


class RoadmapRepository(IRoadmapRepository):
    # Firestore Client には型が存在しないので仕方なく
    db: Any

    def __init__(self, db):
        self.db = db

    def create(self, arg: CreateRoadmap) -> bool:
        doc_ref = self.db.collection(ModelName.roadmaps).document()
        success = doc_ref.set({
            RoadmapKey.id: doc_ref.id,
            RoadmapKey.author_id: arg.author_id,
            RoadmapKey.title: arg.title,
            RoadmapKey.tags: arg.tags,
            RoadmapKey.edges: arg.edges,
            RoadmapKey.vertexes: arg.vertexes,
            RoadmapKey.created_at: datetime.datetime.now(),
            RoadmapKey.updated_at: datetime.datetime.now()
        })

        return success is not None
