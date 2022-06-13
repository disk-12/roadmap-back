from app.model.task import CreateTask
from app.repository.task import ITaskRepository


class TaskService:
    taskRepo: ITaskRepository

    def __init__(self, taskRepo):
        self.taskRepo = taskRepo

    def get_all(self):
        return self.taskRepo.get_all()

    def create(self, arg: CreateTask):
        return self.taskRepo.create(arg)
