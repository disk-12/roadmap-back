import os
from functools import lru_cache
import firebase_admin
from fastapi import FastAPI
from firebase_admin import credentials
from firebase_admin import firestore
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.config import Settings
from .repository.cooud_firestore.task import TaskRepository
from .service.task import TaskService


#
# env 読み出し ->
#


@lru_cache()
def get_settings():
    return Settings()


#
# Firebase 初期化 ->
#

# ローカルであれば serviceAccountKey.json を参照
local = os.getenv("LOCAL", "0")
if local == "1":
    cred = credentials.Certificate(get_settings().service_key)
else:
    cred = credentials.ApplicationDefault()

firebase_admin.initialize_app(cred)

db = firestore.client()

#
# FastAPI 初期化 ->
#

app = FastAPI()

# ミドルウェア
app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#
# FastAPI Repository Service Init ->
#

taskRepo = TaskRepository(db=db)
taskService = TaskService(taskRepo=taskRepo)

#
# FastAPI EndPoint Definition ->
#

# インポートを上に移動すると動作しないので注意
from .router import task

app.include_router(task.router)


@app.get('/')
def read_root():
    pass
