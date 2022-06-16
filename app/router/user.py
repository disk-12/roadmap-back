from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.main import db, taskService, user_service
from app.middleware.auth import get_user_id
from app.model.user import User
from app.service.user import GetMeCommand, CreateUserCommand

router = APIRouter()


class CreateUserRequest(BaseModel):
    name: str


@router.get('/user', response_model=User)
async def show_user(uid=Depends(get_user_id)):
    user = user_service.get_me(GetMeCommand(id=uid))

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


@router.post('/user')
async def create_user(req: CreateUserRequest, uid=Depends(get_user_id)):
    success = user_service.create_user(CreateUserCommand(id=uid, name=req.name))

    if not success:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
