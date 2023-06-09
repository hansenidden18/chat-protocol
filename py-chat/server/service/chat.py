from entity import Group
from controller import UserController, GroupController
from session import Manager, Session

class ChatService:
    instance = None

    @staticmethod
    def get_instance():
        if ChatService.instance is None:
            ChatService.instance = ChatService()
        return ChatService.instance

    def __init__(self):
        self.user_controller = UserController.get_instance()
        self.group_controller = GroupController.get_instance()

    def handle_request(self, session: Session, request, sub_commands: str):
        print(sub_commands)
        commands = sub_commands.split()

        if commands[0] == 'private':
            if commands[1] == 'send':
                self.__send_msg_private_handler(session, request)
            elif commands[1] == 'rcv':
                self.__rcv_msg_private_handler(session, request)
        elif commands[0] == 'group':
            if commands[1] == 'send':
                self.__send_msg_group_handler(session, request)
            elif commands[1] == 'rcv':
                self.__rcv_msg_group_handler(session, request)

    def __rcv_msg_private_handler(self, session: Session, request):
        session.send({
            'To': request['command'],
            'messages': self.user_controller.get_message(session.user.username, request['from_username'])
            # 'messages': session.user.get_inbox_from(request['p_username'])
        })

    def __send_msg_private_handler(self, session: Session, request):
        target_username = request['from_username']
        msg = request['message']

        target_session: Session = Manager.get_user(target_username)
        target_user = self.user_controller.get_username(target_username)

        if target_session is not None:
            target_session.send({
                'To': 'notif',
                'from_user': session.user.username,
                'text': request['message']
            })

        if target_user is not None:
            session.send({
                'To': request['command'],
                'status': 'Success'
            })
        else:
            session.send({
                'To': request['command'],
                'status': 'ERROR',
                'message': 'User not found'
            })

        if target_user is not None:
            message = dict()
            message['from_user'] = session.user.username
            message['text'] = request['message']

            # simpan message di 2 inbox
            session.user.add_inbox(target_user.username, message)
            self.user_controller.insert(session.user)

            target_user.add_inbox(session.user.username, message)
            self.user_controller.insert(target_user)

    def __send_msg_group_handler(self, session: Session, request):

        group_entity: Group = self.group_controller.get_code(request['code'])

        if session.user.username in group_entity.members:
            pass
        else:
            session.send({
                'To': 'message group send',
                'status': 'ERROR',
                'message': 'You are not a member of the group!'
            })
            return

        members = group_entity.members
        for member in members:
            if member == session.user.username:
                continue
            member_session: Session = Manager.get_user(member)
            if member_session is not None:
                member_session.send({
                    'To': 'notif',
                    'from_group': group_entity.name,
                    'from_user': session.user.username,
                    'text': request['message']
                })
                print('send to '+ member_session.user.username)

        group_entity.inbox.append({
            'from_user': session.user.username,
            'text': request['message']
        })

        session.send({
            'To': 'message group send',
            'status': 'Success'
        })

        self.group_repository.save(group_entity)

    def __rcv_msg_group_handler(self, session: Session, request):
        group_entity: Group = self.group_controller.get_code(request['code'])

        if session.user.username in group_entity.members:
            session.send({
                'To': 'message group receive',
                'messages': group_entity.inbox
            })
        else:
            session.send({
                'To': 'message group receive',
                'status': 'ERROR',
                'message': 'You are not a member of the group!'
            })