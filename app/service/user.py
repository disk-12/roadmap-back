from pydantic import BaseModel

from app.model.user import User
from app.repository.user import IUserRepository, FindUser, CreateUser


class GetMeCommand(BaseModel):
    id: str


class CreateUserCommand(BaseModel):
    id: str
    name: str


class UserService:
    userRepo: IUserRepository

    def __init__(self, user_repo):
        self.userRepo = user_repo

    def get_me(self, command: GetMeCommand) -> [User, None]:
        return self.userRepo.get_by_id(arg=FindUser(id=command.id))

    def create_user(self, command: CreateUserCommand) -> bool:
        return self.userRepo.create(arg=CreateUser(id=command.id, name=command.name))
