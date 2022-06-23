from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel

from app.main import user_service
from app.middleware.auth import auth_user
from app.model.user import User
from app.service.user import GetMeCommand, CreateUserCommand, GetUserByIdCommand

router = APIRouter()


class CreateUserRequest(BaseModel):
    name: str


@router.get(
    '/user',
    tags=['users'],
    response_model=User)
async def show_user(uid=Depends(auth_user)):
    user = user_service.get_me(GetMeCommand(id=uid))

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


@router.post('/user',
             tags=['users'],
             status_code=status.HTTP_201_CREATED,
             response_class=Response)
async def create_user(req: CreateUserRequest, uid=Depends(auth_user)):
    success = user_service.create_user(CreateUserCommand(id=uid, name=req.name))

    if not success:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get(
    '/users/{user_id}',
    tags=['users'])
async def get_user(user_id: str):
    return user_service.get_user_by_id(GetUserByIdCommand(id=user_id))
