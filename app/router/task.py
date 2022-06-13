from typing import List

from fastapi import APIRouter

from app.main import db, taskService
from app.model.task import Task, CreateTask

router = APIRouter()


@router.get('/tasks', response_model=List[Task])
async def show():
    return taskService.get_all()


@router.post('/tasks', status_code=201)
def create(arg: CreateTask):
    taskService.create(arg)
    pass
