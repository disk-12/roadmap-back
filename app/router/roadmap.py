from fastapi import Depends, APIRouter, status, Response
from pydantic import BaseModel

from app.main import roadmap_service
from app.middleware.auth import get_user_id
from app.service.roadmap import CreateRoadmapCommand

router = APIRouter()


class CreateRoadmapRequest(BaseModel):
    title: str
    tags: list
    edges: list
    vertexes: list


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
        edges=[],
        vertexes=[],
    ))
