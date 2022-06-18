import datetime

from pydantic import BaseModel

from app.model.user import User
from app.repository.user import IUserRepository, FindUser, CreateUser, UpdateUser


class GetMeCommand(BaseModel):
    id: str


class CreateUserCommand(BaseModel):
    id: str
    name: str


class GetUserByIdCommand(BaseModel):
    id: str


class UserService:
    userRepo: IUserRepository

    def __init__(self, user_repo):
        self.userRepo = user_repo

    def get_me(self, command: GetMeCommand) -> [User, None]:
        user = self.userRepo.get_by_id(arg=FindUser(id=command.id))

        # 最終ログイン日付を更新
        if user is not None:
            self.userRepo.update(UpdateUser(id=command.id, last_login_at=datetime.datetime.now()))
        else:
            return None

        return user

    def get_user_by_id(self, command: GetUserByIdCommand):
        return self.userRepo.get_by_id(arg=FindUser(id=command.id))

    def create_user(self, command: CreateUserCommand) -> bool:
        return self.userRepo.create(arg=CreateUser(id=command.id, name=command.name))
