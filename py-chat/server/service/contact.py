from controller import UserController
from session import Session


class ContactService:

    def __init__(self):
        self.user_controller = UserController()

    def handle_request(self, session: Session, request: dict, sub_commands: str):
        user = session.user
        response = dict()
        response['To'] = request['command']
        commands = sub_commands.split('')

        if commands[0] == 'get':
            response['contacts'] = user.contacts
            session.send(response)

        elif commands[0] == 'add':
            self.__add_contact(session, request)

        elif commands[0] == 'del':
            self.__del_contact(session, request)

    def __add_contact(self, session: Session, request: dict):
        new_contacts = request['contacts']
        contact_list = session.user.contacts
        counter = 0
        for contact in new_contacts:
            if contact not in contact_list \
                    and self.user_controller.get_username(contact) \
                    and contact != session.user.username:
                contact_list.append(contact)
                counter += 1

        self.user_controller.insert(session.user)
        response = dict()
        response['To'] = request['command']
        response['message'] = str(counter) + ' new contact added'

        session.send(response)

    def __del_contact(self, session: Session, request: dict):
        target_contacts = request['contacts']
        contact_list = session.user.contacts
        counter = 0
        for contact in target_contacts:
            if contact in contact_list:
                contact_list.remove(contact)
                counter += 1

        self.user_controller.insert(session.user)
        response = dict()
        response['To'] = request['command']
        response['message'] = str(counter) + ' contact deleted'

        session.send(response)
