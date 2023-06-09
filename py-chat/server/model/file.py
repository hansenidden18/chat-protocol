from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue

class FileModel():
    __tablename__ = 'file'

    id = Column('id', String(36), primary_key = True, autoincrement = False, server_default = FetchedValue())
    owner = Column('owner', String(128), nullable = False)
    file_code = Column('file_code', String(36))
    file_path = Column('file_path', String(64))