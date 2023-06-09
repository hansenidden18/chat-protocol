import json
import socket
import entity

class Manager:
    sessions = []

    @staticmethod
    def get_user(username):
        print(Manager.sessions)
        for session in Manager.sessions:
            print(session.user.username)
            if session.user.username == username:
                return session
        return None
    
    @staticmethod
    def add_session(session):
        Manager.sessions.append(session)

    @staticmethod
    def del_sesion(session):
        if session in Manager.sessions:
            Manager.sessions.remove(session)

class Session:
    connection: socket.socket
    user: entity.User

    def __init__(self):
        self.connection = None
        self.user = None
        self.token = None
    
    def connect(self, connection: socket.socket):
        self.connection = connection
    
    def login(self, user: entity.User):
        self.user = user
        Manager.add_session(self)
    
    def send(self, response):
        print('send >')
        print(response)
        if isinstance(response, dict):
            self.connection.sendall(json.dumps(response).encode())
        else:
            self.connection.sendall(response.encode())
    
    def clear(self):
        self.user = None
        self.token = None
