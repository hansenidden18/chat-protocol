from entity import Entity, Group
from model import GroupModel
from controller import BaseController

class GroupController(BaseController):
    instance = None

    @staticmethod
    def get_instance():
        if GroupRepository.instance is None:
            GroupRepository.instance = GroupRepository()
        return GroupRepository.instance

    def __init__(self):
        super().__init__('groups')
        self.db = db_session()

    def get_code(self, code: str) -> Group:
        data = self.db.execute(select(GroupModel).where(GroupModel.code == code)).scalar()

        if data is None:
            return None
        else:
            group = Group()
            group.id = data.id
            group.name = data.name
            group.inbox = data.inbox
            group.members = data.members
            group.admins = data.admins
            group.code = data.code
            return group

    def get_name(self, name):
        data = self.db.execute(select(GroupModel).where(GroupModel.name == name)).scalar()
        if data is not None:
            group = Group()
            group.id = data.id
            group.name = data.name
            group.inbox = data.inbox
            group.members = data.members
            group.admins = data.admins
            group.code = data.code
            return group
        return None
    
    def insert(self, obj: entity.Entity):
        if obj.id is None:
            group = GroupModel()
            group.name = obj.name
            group.inbox = obj.inbox
            group.members = obj.members
            group.admins = obj.admins
            group.code = obj.code
        else:
            group = self.db.get(GroupModel, obj.id)
            group.name = obj.name
            group.inbox = obj.inbox
            group.members = obj.members
            group.admins = obj.admins
            group.code = obj.code
        self.db.add(group)
        self.db.commit()
        data = self.db.execute(select(GroupModel).where(GroupModel.name == obj.name)).scalar()
        return data.id