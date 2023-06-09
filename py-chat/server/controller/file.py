import entity
from entity import File
from controller import BaseController
from sqlalchemy import select
from model import FileModel

class FileController(BaseController):
    instance = None

    @staticmethod
    def get_instance():
        if FileController.instance is None:
            FileController.instance = FileController()
        return FileController.instance

    def __init__(self):
        super().__init__(('files'))
        self.db = BaseController.db_session(self)
    
    def find_code(self, file_code):
        data = self.db.execute(select(FileModel).where(FileModel.file_code == file_code)).scalar()
        if data is not None:
            file = File()
            file.id = data.id
            file.file_code = data.file_code
            file.file_path = data.file_path
            file.owner = data.owner
            return file
        return None
    
    def insert(self, obj: entity.BaseEntity):
        if obj.id is None:
            file = FileModel()
            file.file_code = obj.file_code
            file.file_path = obj.file_path
            file.owner = obj.owner
        else:
            file = self.db.get(FileModel, obj.id)
            file.file_code = obj.file_code
            file.file_path = obj.file_path
            file.owner = obj.owner
        self.db.add(file)
        self.db.commit()
        data = self.db.execute(select(FileModel).where(FileModel.file_code == obj.file_code)).scalar()
        return data.id