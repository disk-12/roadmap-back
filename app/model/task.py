from pydantic import BaseModel


class CreateTask(BaseModel):
    name: str


class Task(BaseModel):
    id: str
    name: str

    @staticmethod
    def from_dict(source):
        task = Task(id=source[u'id'], name=source[u'name'])
        return task
