import json
import os
import uuid

from entity import File, Group
from controller import UserController, FileController, GroupController
from session import Session, Manager


class FileService:
    instance = None

    @staticmethod
    def get_instance():
        if FileService.instance is None:
            FileService.instance = FileService()
        return FileService.instance

    def __init__(self):
        self.group_controller = GroupController.get_instance()
        self.user_controller = UserController.get_instance()
        self.file_controller = FileController.get_instance()

    def handle_request(self, session: Session, request, sub_commands: str):
        commands = sub_commands.split('')

        if commands[0] == 'private':
            if commands[1] == 'send':
                self.__send_private_file_handle(session, request)
            elif commands[1] == 'rcv':
                self.__rcv_file_handle(session, request)

        elif commands[0] == 'group':
            if commands[1] == 'send':
                self.__send_group_file_handle(session, request)
            elif commands[1] == 'rcv':
                self.__rcv_file_handle(session, request)

    def __send_group_file_handle(self, session: Session, request):
        group_entity: Group = self.group_controller.get_code(request['code'])

        if session.user.username in group_entity.members:
            pass
        else:
            session.send({
                'To': 'file group send',
                'status': 'ERROR',
                'message': 'You are not a member of the group!'
            })
            return

        session.send({
            'To': 'file group send',
            'status': 'Ready'
        })

        file_entity: File = self.__send_file_handle(session, request)

        message = {
            'text': '[' + request['file_name'] + '], file_code: ' + file_entity.file_code,
            'from_user': session.user.username
        }

        group_entity.inbox.append(message)
        self.group_controller.insert(group_entity)

        message['To'] = 'notif'
        message['from_group'] = group_entity.name

        members = group_entity.members
        for member in members:
            if member == session.user.username:
                continue
            member_session: Session = Manager.get_user(member)
            if member_session is not None:
                member_session.send(message)
                print('send to ' + member_session.user.username)

        session.send({
            'To': 'message group send',
            'status': 'Success'
        })

    def __send_private_file_handle(self, session: Session, request):
        from_user = self.user_controller.get_username(request['from_username'])

        if from_user is None:
            session.send({
                'To': 'file private send',
                'status': 'Rejected',
                'message': 'User not exist'
            })
            return

        session.send({
            'To': 'file private send',
            'status': 'Ready'
        })

        file_entity: File = self.__send_file_handle(session, request)

        message = {
            'text': '[' + request['file_name'] + '], file_code: ' + file_entity.file_code,
            'from_user': session.user.username
        }

        from_user.add_inbox(session.user.username, message)
        session.user.add_inbox(from_user.username, message)
        self.user_controller.insert(from_user)
        self.user_controller.insert(session.user)

        message['To'] = 'notif'
        target_session: Session = Manager.get_user(from_user.username)
        if target_session is not None:
            target_session.send(message)

        session.send(message)

    def __send_file_handle(self, session: Session, request: dict) -> FileEntity:

        unique_code = str(uuid.uuid4())[1:7]
        file_path = 'storage/' + unique_code + '-' + request['file_name']
        fd = open(file_path, 'wb+', 0)

        max_size = request['file_size']
        received = 0

        conn = session.connection
        while received < max_size:
            data = conn.recv(1024)
            print('receive')
            received += len(data)
            fd.write(data)

        fd.close()

        file_entity = File()
        file_entity.owner = session.user.username
        file_entity.file_path = file_path
        file_entity.file_code = unique_code

        self.file_controller.insert(file_entity)
        return file_entity

    def __rcv_file_handle(self, session: Session, request):

        file_entity = self.file_controller.find_code(request['file_code'])

        if file_entity is None or not os.path.exists(file_entity.file_path):
            session.send({
                'To': request['command'],
                'status': 'ERROR',
                'message': 'file not found!'
            })
        else:
            file_name = file_entity.file_path.split('/')[1]
            file_path = file_entity.file_path
            fd = open(file_path, 'rb')
            session.send({
                'To': request['COMMAND'],
                'status': 'success',
                'file_name': file_name,
                'file_size': os.path.getsize(file_path)
            })

            resp = json.loads(session.connection.recv(1024).decode('utf-8'))

            if resp['status'] == 'Ready':
                for data in fd:
                    session.connection.sendall(data)

                fd.close()
