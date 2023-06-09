from handler import BaseHandler
from service import *

from session import Session


class CoreHandler(BaseHandler):
    instance = None

    @staticmethod
    def get_instance():
        if CoreHandler.instance is None:
            CoreHandler.instance = CoreHandler()
        return CoreHandler.instance

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
            pass