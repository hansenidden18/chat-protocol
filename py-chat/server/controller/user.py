from controller import BaseController
from entity import User
from model import UserModel
from sqlalchemy import select

class UserController(BaseController):
    instance = None

    @staticmethod
    def get_instance():
        if UserRepository.instance is None:
            UserRepository.instance = UserRepository()
        return UserRepository.instance
    
    def __init__(self):
        super().__init__('user')
        self.db = db_session()
    
    def get_username(self, username):
        data = self.db.execute(select(UserModel).where(UserModel.username == username)).scalar()

        if data is not None:
            user = User()
            user.id = data.id
            user.username = data.username
            user.password = data.password
            user.contacts = data.contacts
            user.inbox = data.inbox
            user.groups = data.groups
            return user
        return None
    
    def get_message(self, username, from_user):
        data = self.db.execute(select(UserModel).where(UserModel.username == username)).scalar()

        if from_user in data.inbox.keys():
            return data.inbox[from_user]
        else:
            return []
    
    def insert(self, obj: entity.Entity):
        if obj.id is None:
            user = UserModel()
            user.name = obj.name
            user.inbox = obj.inbox
            user.members = obj.members
            user.admins = obj.admins
            user.code = obj.code
        else:
            user = self.db.get(UserModel, obj.id)
            user.name = obj.name
            user.inbox = obj.inbox
            user.members = obj.members
            user.admins = obj.admins
            user.code = obj.code
        self.db.add(user)
        self.db.commit()
        data = self.db.execute(select(UserModel).where(UserModel.name == obj.name)).scalar()
        return data.id

    def add_group(self, username, group):
        data = self.db.execute(select(UserModel).where(UserModel.username == username)).scalar()

        data.username = username
        data.groups = group

        self.db.add(data)
        db.commit()