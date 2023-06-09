from entity import Entity

class User(Entity):
    def __init__(self):
        super().__init__()
        self.username = None
        self.password = None

        self.groups = []
        self.contacts = []
        self.inbox = {}
    
    def add_inbox(self, user, message):
        if user not in self.inbox.keys():
            self.inbox[user] = []
        self.inbox[user].append(message)

    def get_inbox(self, user):
        if user not in self.inbox.keys():
            return [None]
        return self.inbox[user]
    
    def get_data(self):
        return {
            'username': self.username,
            'password': self.password,
            'groups': self.groups,
            'contacts': self.contacts,
            'inbox': self.inbox
        }