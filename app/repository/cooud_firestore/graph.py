import datetime
from typing import Any, List

from app.model.edge import EdgeKey, Edge
from app.model.graph import GraphKey, Graph
from app.model.vertex import VertexKey, Vertex, VertexType
from app.repository.cooud_firestore.model import ModelName
from app.repository.graph import IGraphRepository, UpdateGraph, CreateGraph


class GraphRepository(IGraphRepository):
    # Firestore Client には型が存在しないので仕方なく
    db: Any

    def __init__(self, db):
        self.db = db

    def get_by_id(self, roadmap_id: str) -> Graph:
        graph = self.db.collection(ModelName.graphs).document(roadmap_id).get()
        graph_dict = graph.to_dict()

        vertex_ary = graph_dict[GraphKey.vertexes].values()
        edge_ary = graph_dict[GraphKey.edges].values()

        vertexes: List[Vertex] = []
        for vertex in vertex_ary:
            vertexes.append(
                Vertex.from_dict({**vertex, VertexKey.achieved: False})
            )

        edges: List[Edge] = []
        for edge in edge_ary:
            edges.append(
                Edge.from_dict(edge)
            )

        return Graph.from_dict({
            **graph_dict,
            GraphKey.vertexes: vertexes,
            GraphKey.edges: edges
        })

    def create(self, arg: CreateGraph) -> bool:
        doc_ref = self.db.collection(ModelName.graphs).document(arg.id)

        edge_ary: dict = {}
        for edge in arg.edges:
            edge_ary[edge.id] = {
                EdgeKey.id: edge.id,
                EdgeKey.source_id: edge.source_id,
                EdgeKey.target_id: edge.target_id,
                EdgeKey.is_solid_line: edge.is_solid_line,
            }

        vertex_ary: dict = {}
        for vertex in arg.vertexes:
            if vertex.type == VertexType.default:
                vertex_ary[vertex.id] = {
                    VertexKey.id: vertex.id,
                    VertexKey.type: vertex.type,
                    VertexKey.x_coordinate: vertex.x_coordinate,
                    VertexKey.y_coordinate: vertex.y_coordinate
                }

            if vertex.type == VertexType.youtube:
                vertex_ary[vertex.id] = {
                    VertexKey.id: vertex.id,
                    VertexKey.type: vertex.type,
                    VertexKey.x_coordinate: vertex.x_coordinate,
                    VertexKey.y_coordinate: vertex.y_coordinate,
                    VertexKey.youtube_id: vertex.youtube_id,
                    VertexKey.youtube_start: vertex.youtube_start,
                    VertexKey.youtube_end: vertex.youtube_end
                }

            if vertex.type == VertexType.link:
                vertex_ary[vertex.id] = {
                    VertexKey.id: vertex.id,
                    VertexKey.type: vertex.type,
                    VertexKey.x_coordinate: vertex.x_coordinate,
                    VertexKey.y_coordinate: vertex.y_coordinate,
                    VertexKey.link: vertex.link,
                }

        success = doc_ref.set({
            GraphKey.id: doc_ref.id,
            GraphKey.edges: edge_ary,
            GraphKey.vertexes: vertex_ary,
            GraphKey.created_at: datetime.datetime.now(),
            GraphKey.updated_at: datetime.datetime.now(),
        })

        return success is not None

    def update(self, arg: UpdateGraph) -> bool:
        doc_ref = self.db.collection(ModelName.graphs).document(arg.id)

        # NOTE:
        # dict を作成し None の項目があるなら削除
        # None の項目で上書きしてしまうとデータベース上で Null になってしまう
        new_items = {k: v for k, v in arg.dict().items() if v is not None}

        # array を dict に変換
        if arg.edges is not None:
            edge_dict: dict = {}
            for edge in arg.edges:
                edge_dict[edge.id] = {
                    EdgeKey.id: edge.id,
                    EdgeKey.source_id: edge.source_id,
                    EdgeKey.target_id: edge.target_id,
                    EdgeKey.is_solid_line: edge.is_solid_line,
                }
            new_items[GraphKey.edges] = edge_dict

        # array を dict に変換
        if arg.vertexes is not None:
            vertex_dict: dict = {}
            for vertex in arg.vertexes:
                vertex_dict[vertex.id] = {
                    VertexKey.id: vertex.id,
                    VertexKey.x_coordinate: vertex.x_coordinate,
                    VertexKey.y_coordinate: vertex.y_coordinate
                }
            new_items[GraphKey.vertexes] = vertex_dict

        success = doc_ref.update(new_items)

        return success is not None
