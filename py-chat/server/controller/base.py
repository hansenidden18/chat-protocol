import entity
from model import UserModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

class BaseController:
    engine = None
    def __init__(self, entity_name):
        
        if BaseController.engine is None:
            self.engine = create_engine("postgresql+psycopg2://posgres:user@postgres:5432/python_docker", future=True)
        self.db = Session(self.engine)
    
    def db_session(self):
        return Session(BaseController.engine)
    

