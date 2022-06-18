from typing import List, Union

from fastapi import Depends, APIRouter, status, Response
from pydantic import BaseModel

from app.main import roadmap_service, user_favorite_service
from app.middleware.auth import get_user_id
from app.model.edge import Edge
from app.model.roadmap import Roadmap
from app.model.vertex import Vertex
from app.service.roadmap import CreateRoadmapCommand, UpdateRoadmapCommand
from app.service.user_favorite import AddFavoriteCommand, DeleteFavoriteCommand

router = APIRouter()


class CreateRoadmapRequest(BaseModel):
    title: str
    tags: list
    edges: List[Edge]
    vertexes: List[Vertex]


class UpdateRoadmapRequest(BaseModel):
    title: Union[str, None]
    tags: Union[list, None]
    edges: Union[List[Edge], None]
    vertexes: Union[List[Vertex], None]


# NOTE:
# response_class に Response を指定すると Swagger 上で Null になる
@router.post('/roadmaps', status_code=status.HTTP_201_CREATED, response_class=Response)
async def create_roadmap(req: CreateRoadmapRequest, uid=Depends(get_user_id)):
    # TODO(k-shir0): エラーハンドリング
    roadmap_service.create(CreateRoadmapCommand(
        author_id=uid,
        title=req.title,
        # TODO(k-shir0): 入力するようにする
        tags=[],
        edges=req.edges,
        vertexes=req.vertexes,
    ))


@router.get('/roadmaps/{roadmap_id}', response_model=Roadmap)
async def show_roadmap(roadmap_id: str):
    return roadmap_service.get_by_id(roadmap_id)


@router.patch('/roadmaps/{roadmap_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def patch_roadmap(roadmap_id: str, req: UpdateRoadmapRequest, _=Depends(get_user_id)):
    roadmap_service.update(command=UpdateRoadmapCommand(
        id=roadmap_id,
        **req.dict()
    ))


@router.post('/roadmaps/{roadmap_id}/favorite', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def post_add_favorite(roadmap_id: str, uid=Depends(get_user_id)):
    user_favorite_service.add_favorite(AddFavoriteCommand(
        user_id=uid,
        roadmap_id=roadmap_id,
    ))


@router.delete('/roadmaps/{roadmap_id}/favorite', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def post_delete_favorite(roadmap_id: str, uid=Depends(get_user_id)):
    user_favorite_service.delete_favorite(DeleteFavoriteCommand(
        user_id=uid,
        roadmap_id=roadmap_id,
    ))


@router.get('/home_timeline', response_model=List[Roadmap])
async def get_home_timeline():
    return roadmap_service.get_roadmaps_by_newest()
