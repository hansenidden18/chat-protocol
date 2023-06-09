from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue

class UserModel():
    __tablename__ = 'user'

    id = Column('id', String(36), primary_key = True, autoincrement = False, server_default = FetchedValue())
    username = Column('username', String(128), nullable = False)
    password = Column('password', String(64), nullable = False)
    contacts = Column('contact', String(64))
    inbox = Column('contact', JSON)

    groups = relationship('Group')