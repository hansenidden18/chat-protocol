import uuid

from entity import User
from .base import BaseHandler
from controller import UserController
from session import Session

class AuthHandler(BaseHandler):
    instance = None

    @staticmethod
    def get_instance():
        if AuthHandler.instance is None:
            AuthHandler.instance = AuthHandler()
        return AuthHandler.instance

    def __init__(self):
        super().__init__()
        self.tokens_data = {}
        self.data = UserController.get_instance()
    
    def handle(self, session, request):
        command = request['command']

        if command is None:
            session.send({
                'To': request['command'],
                'status': 'ERROR',
                'message': 'Unknown request!!!'
            })
        
        cmd = command.split()
        if cmd[0] == 'auth':
            j = cmd[1]

            if j == 'login':
                self.login(session, request)
            if j == 'logout':
                self.logout(session, request)
            if j == 'register':
                self.register(session, request)
        elif self.authorized(session, request):
            super(AuthHandler, self).handle(session, request)
        else:
            session.send({
                'status': 'ERROR',
                'message':'Unauthorized!!!'
            })
        
    def authorized(self, session: Session, request):
        if 'token' not in request.keys():
            return False
        
        token = request['token']

        if token is '' or token is None:
            return False

        return session.token == token
    
    def login(self, session: Session, request):
        username = request['username']
        password = request['password']
        if username is None or password is None:
            session.send({
                'To': 'Login',
                'Status': 'ERROR',
                'message': 'Username or Password is Empty'
            })
        
        user - self.data.get_username(username)

        if user is None:
            session.send({
                'To': request['command'],
                'status': 'ERROR',
                'message': 'Unknown User'
            })
        
        if user.password == password:
            session.login(user)
            session.token = str(uuid.uuid4())
            session.send_response({
                'To': request['command'],
                'status': 'Success',
                'message': 'Login Success',
                'token': session.token
            })
        else:
            session.send({
                'To': request['command'],
                'status': 'ERROR',
                'message': 'Wrong Password'
            })

    def logout(self, session: Session, request):
        if self.authorized(session, request):
            session.clear()
            session.send({
                'To': request['command'],
                'status': 'Success',
                'message': 'Logging Out'
            })
        else:
            session.send({
                'To': request['command'],
                'status': 'ERROR',
                'message': 'unauthorized!!!'
            })

    def register(self, session: Session, request):
        username = request['username']
        password = request['password']
        confirm_password = request['confirm_password']

        if username is None or password is None or confirm_password is None:
            session.send({
                'To': request['command'],
                'status': 'ERROR',
                'message': 'Username and Password can\'t be empty'
            })
            return False

        if password != confirm_password:
            session.send({
                'To': request['command'],
                'status': 'ERROR',
                'message': 'Password doesn\'t match!'
            })
            return False

        user = self.data.get_username(username)

        if user is None:
            user = User()
            user.username = username
            user.password = password1
            self.data.save(user)
            session.send_response({
                'To': request['command'],
                'status': 'Success',
                'message': 'Register Success'
            })
        else:
            session.send_response({
                'To': request['command'],
                'status': 'ERROR',
                'message': 'Username exist!!!'
            })

