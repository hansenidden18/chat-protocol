from handler import BaseHandler
from services import *

from session import Session


class CoreHandler(AbstractHandler):

    def __init__(self):
        super().__init__()
        self.services = {
            'contact': ContactService(),
            'group': GroupService(),
            'message': ChatService(),
            'file': FileService()
        }

    def handle(self, session: Session, request):
        commands: str = request['command'].split(' ', 1)
        try:
            self.services[commands[0]].handle_request(session, request, commands[1])
        except Exception as e:
            continue