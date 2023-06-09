from entity import BaseEntity

class File(BaseEntity):
    def __init__(self):
        super().__init__()
        self.owner = None
        self.file_code = None
        self.file_path = None
    
    def get_data(self):
        return {
            'owner': self.owner,
            'file_code': self.file_code,
            'file_path': self.file_path
        }