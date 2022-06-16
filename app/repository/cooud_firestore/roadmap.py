import datetime
from typing import Any

from app.model.edge import EdgeKey, Edge
from app.model.roadmap import RoadmapKey
from app.model.vertex import VertexKey
from app.repository.cooud_firestore.model import ModelName
from app.repository.roadmap import IRoadmapRepository, CreateRoadmap


class RoadmapRepository(IRoadmapRepository):
    # Firestore Client には型が存在しないので仕方なく
    db: Any

    def __init__(self, db):
        self.db = db

    def create(self, arg: CreateRoadmap) -> bool:
        doc_ref = self.db.collection(ModelName.roadmaps).document()
        roadmap = doc_ref.set({
            RoadmapKey.id: doc_ref.id,
            RoadmapKey.author_id: arg.author_id,
            RoadmapKey.title: arg.title,
            RoadmapKey.created_at: datetime.datetime.now(),
            RoadmapKey.updated_at: datetime.datetime.now()
        })

        if roadmap is None:
            return False

        batch = self.db.batch()
        graph_ref = self.db.collection(ModelName.graphs).document(doc_ref.id)
        for edge in arg.edges:
            edge_ref = graph_ref.collection(ModelName.edges).document(edge.id)
            batch.set(edge_ref, {
                EdgeKey.id: edge.id,
                EdgeKey.source_id: edge.source_id,
                EdgeKey.target_id: edge.target_id,
            })

        for vertex in arg.vertexes:
            vertex_ref = graph_ref.collection(ModelName.vertexes).document(vertex.id)
            batch.set(vertex_ref, {
                VertexKey.id: vertex.id,
                VertexKey.x_coordinate: vertex.x_coordinate,
                VertexKey.y_coordinate: vertex.y_coordinate,
            })

        success = batch.commit()

        return success is not None
