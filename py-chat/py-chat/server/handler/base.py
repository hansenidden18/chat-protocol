from session import Session

class BaseHandler(object):
    
    def __init__(self):
        self.next_handler = None
    
    def handle_next(self, handler):
        self.next_handler = handler
    
    def handle(self, session: Session, request):
        '''
        :session:
        :request <dict>:
        '''
        if self.next_handler is not None:
            self.next_handler.handle(session, request)