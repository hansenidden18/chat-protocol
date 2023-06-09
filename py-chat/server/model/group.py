from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue

class GroupModel():
    __tablename__ = 'group'

    id = Column('id', String(36), primary_key = True, autoincrement = False, server_default = FetchedValue())
    name = Column('name', String(128), nullable = False)
    code = Column('code', String(36), nullable = False)
    inbox = Column('inbox', String(64))

    members = relationship('User')
    admins = relationship('User')
    contacts = relationship('User')