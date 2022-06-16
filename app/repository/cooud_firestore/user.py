import datetime
from typing import Any

from app.model.user import User, UserKey
from app.repository.cooud_firestore.model import ModelName
from app.repository.user import IUserRepository, FindUser, CreateUser, UpdateUser


class UserRepository(IUserRepository):
    # Firestore Client には型が存在しないので仕方なく
    db: Any

    def __init__(self, db):
        self.db = db

    def get_by_id(self, arg: FindUser) -> [User, None]:
        docs = self.db.collection(ModelName.users).document(arg.id).get()

        if not docs.exists:
            return None

        return User.from_dict(docs.to_dict())

    def create(self, arg: CreateUser) -> bool:
        # ユーザ重複チェック
        user = self.get_by_id(FindUser(id=arg.id))
        if user is not None:
            return False

        doc_ref = self.db.collection(ModelName.users).document(arg.id)
        success = doc_ref.set({
            UserKey.id: arg.id,
            UserKey.name: arg.name,
            UserKey.last_login_at: datetime.datetime.now(),
            UserKey.created_at: datetime.datetime.now(),
            UserKey.updated_at: datetime.datetime.now()
        })

        return success is not None

    def update(self, arg: UpdateUser) -> bool:
        doc_ref = self.db.collection(ModelName.users).document(arg.id)

        # None:
        # dict を作成し None の項目があるなら削除
        # None の項目で上書きしてしまうとデータベース上で Null になってしまう
        tmp = {
            UserKey.name: arg.name,
            UserKey.last_login_at: arg.last_login_at,
            UserKey.updated_at: datetime.datetime.now(),
        }
        new_dic = {k: v for k, v in tmp.items() if v is not None}

        success = doc_ref.update(new_dic)

        return success is not None
