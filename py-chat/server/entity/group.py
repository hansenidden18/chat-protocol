from entity import BaseEntity

class Group(BaseEntity):
    def __init__(self):
        self.name = None
        self.code = None
        self.admin = []
        self.member = []
        self.inbox = []
        self.active = True
    
    def get_data(self):
        return {
            'name': self.name,
            'admin': self.admin,
            'member': self.member,
            'inbox': self.inbox,
            'code': self.code
        }
        