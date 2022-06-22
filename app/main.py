import os
from functools import lru_cache

import firebase_admin
from algoliasearch.search_client import SearchClient
from fastapi import FastAPI
from firebase_admin import credentials
from firebase_admin import firestore
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.config import Settings
from .repository.algolia.roadmap_search import RoadmapSearchRepository
from .repository.cooud_firestore.graph import GraphRepository
from .repository.cooud_firestore.roadmap import RoadmapRepository
from .repository.cooud_firestore.task import TaskRepository
from .repository.cooud_firestore.user import UserRepository
from .repository.cooud_firestore.user_achievement import UserAchievementRepository
from .repository.cooud_firestore.user_favorite import UserFavoriteRepository
from .service.roadmap import RoadmapService
from .service.task import TaskService

#
# env 読み出し ->
#
from .service.user import UserService
from .service.user_achievement import UserAchievementService
from .service.user_favorite import UserFavoriteService


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
# Algolia 初期化
#

client = SearchClient.create(get_settings().algolia_app_id, get_settings().algolia_app_key)

#
# FastAPI Repository And Service Init ->
#


taskRepo = TaskRepository(db=db)
user_repo = UserRepository(db=db)
user_favorite_repo = UserFavoriteRepository(db=db)
user_achievement_repo = UserAchievementRepository(db=db)
roadmap_repo = RoadmapRepository(db=db)
roadmap_search_repo = RoadmapSearchRepository(client=client)
graph_repo = GraphRepository(db=db)

taskService = TaskService(taskRepo=taskRepo)
user_service = UserService(user_repo=user_repo)
user_achievement_service = UserAchievementService(
    user_achievement_repo=user_achievement_repo,
    graph_repo=graph_repo
)
user_favorite_service = UserFavoriteService(
    user_favorite_repo=user_favorite_repo,
    roadmap_repo=roadmap_repo
)
roadmap_service = RoadmapService(
    roadmap_repo=roadmap_repo,
    graph_repo=graph_repo,
    user_favorite_repo=user_favorite_repo,
    user_achievement_repo=user_achievement_repo,
    roadmap_search_repo=roadmap_search_repo
)

#
# FastAPI EndPoint Definition ->
#

# インポートを上に移動すると動作しないので注意
from .router import task, user, roadmap

app.include_router(task.router)
app.include_router(user.router)
app.include_router(roadmap.router)


@app.get('/')
def read_root():
    pass
