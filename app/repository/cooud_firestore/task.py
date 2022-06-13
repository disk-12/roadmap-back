from typing import Any
from fastapi import HTTPException

from app.model.task import Task
from app.repository.task import ITaskRepository


class TaskRepository(ITaskRepository):
    # Firestore Client には型が存在しないので仕方なく
    db: Any

    def __init__(self, db):
        self.db = db

    def get_all(self):
        docs = self.db.collection(u'tasks').get()

        ary = []
        for doc in docs:
            ary.append(Task.from_dict(doc.to_dict()))

        if len(ary) == 0:
            raise HTTPException

        return ary

    def create(self, arg):
        doc_ref = self.db.collection(u'tasks').document()
        success = doc_ref.set({
            u'id': doc_ref.id,
            u'name': arg.name,
        })

        return success is not None
