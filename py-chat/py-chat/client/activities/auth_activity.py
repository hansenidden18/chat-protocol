import socket

from activities import MainMenuActivity, AbstractActivity
from activities.activity_container import ActivityContainer


class AuthActivity(AbstractActivity):

    instance = None

    @staticmethod
    def get_instance(connection: socket.socket, container: ActivityContainer = None):
        if AuthActivity.instance is None:
            AuthActivity.instance = AuthActivity(connection)
            AuthActivity.instance.set_container(container)
        return AuthActivity.instance

    def get_activity_input_line(self):
        return 'Auth Menu > '

    def show_menu(self):
        print('========Instruction===========')
        print('login <username> <password>')
        print('register <username> <password> <retyped-password>')
        print('logout')
        print('==============================\n')

    def handle_input(self, args: str):
        args = args.split(' ')

        request = dict()
        if args[0] == 'login':
            request['command'] = 'auth login'
            request['username'] = args[1]
            request['password'] = args[2]

            self.send_request(request)
            self.set_username(args[1])

        elif args[0] == 'register':
            request['command'] = 'auth register'
            request['username'] = args[1]
            request['password'] = args[2]
            request['confirm_password'] = args[3]

            self.send_request(request)

        elif args[0] == 'logout':
            request['command'] = 'auth logout'

            self.send_request(request)

        else:
            if args[0] != 'help':
                print('<UNKNOWN COMMAND>')
            self.show_menu()
            return

    def response_handler(self, response, is_json):
        if is_json:
            if response['To'] == 'auth login':
                print(response['message'])
                if response['status'] == 'Success':
                    self.set_token(response['token'])
                    next_activity = MainMenuActivity.get_instance(self.connection, self.activity_container)
                    next_activity.set_from_activity(self)
                    self.move_activity(next_activity)
            elif response['To'] == 'auth logout':
                print(response['message'])
                if response['status'] == 'Success':
                    self.set_token(None)
            else:
                print(response['message'])

