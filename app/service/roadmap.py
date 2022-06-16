from pydantic import BaseModel

from app.repository.roadmap import IRoadmapRepository, CreateRoadmap


class CreateRoadmapCommand(BaseModel):
    author_id: str
    title: str
    tags: list
    edges: list
    vertexes: list


class RoadmapService:
    roadmap_repo: IRoadmapRepository

    def __init__(self, roadmap_repo: IRoadmapRepository):
        self.roadmap_repo = roadmap_repo

    def create(self, command: CreateRoadmapCommand):
        return self.roadmap_repo.create(CreateRoadmap(
            author_id=command.author_id,
            title=command.title,
            tags=command.tags,
            edges=command.edges,
            vertexes=command.vertexes,
        ))

    def get_by_id(self, roadmap_id: str):
        return self.roadmap_repo.get_by_id(roadmap_id)
