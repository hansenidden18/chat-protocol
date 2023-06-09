import uuid

from entity import Group, User
from controller import GroupController, UserController
from session import Session


class GroupService:
    def __init__(self):
        self.user_controller = UserController.get_instance()
        self.group_repository = GroupController.get_instance()
        pass

    def handle_request(self, session: Session, request, commands: str):
        commands = commands.split('')

        if commands[0] == 'invite':
            self.__handle_invite(session, request)
        elif commands[0] == 'rcv':
            self.__get_group(session, request)
        elif commands[0] == 'create':
            self.__create_group(session, request)
        elif commands[0] == 'join':
            self.__join_group(session, request)
        elif commands[0] == 'exit': 
            self.__exit_group(session, request)

    def __handle_invite(self, session, request):
        request_code = request['code']
        group = self.group_controller.get_code(request_code)
        group_code = group.code
        group_name = group.name
        username = session.user.username
        group_members = group.members
        if username not in group_members:
            session.send({
                'To': 'group invite',
                'status': 'ERROR',
                'message': 'You are not a member of this group'
            })

        else:
            group_invite = {
                'code': group_code,
                'group_name': group_name
            }

            request_user = request['user_list']
            new_member = []
            for name in request_user:
                user_exist = self.user_controller.get_username(name)
                if user_exist is not None:
                    user_group = user_exist.group_list
                    user_group.append(group_invite)
                    self.user_controller.save(user_exist)
                    new_member.append(name)
                    session.send({
                        'To': 'group invite',
                        'status': 'Success',
                        'message': name + ' has joined this group'
                    })
                else:
                    session.send({
                        'To': 'group invite',
                        'status': 'Error',
                        'message': name + ' failed to join this group'
                    })

            if len(new_member) > 0:
                group_members.extend(new_member)
                self.group_controller.insert(group)
                session.send({
                    'To': 'group invite',
                    'status': 'Success',
                    'message': 'New members have been added'
                })
            else:
                session.send({
                    'To': 'group invite',
                    'status': 'ERROR',
                    'message': 'No member added'
                })

    def __get_group(self, session: Session, request):
        user_entity: User = self.user_controller.get_username(session.user.username)

        session.send({
            'To': 'group get',
            'groups': user_entity.groups
        })

    def __create_group(self, session: Session, request):
        user = [session.user.username]
        group_name = request['group_name']

        group = Group()
        group.name = group_name
        # if request['code'] is not None:
        #     group.code = request['code']
        unique_code = str(uuid.uuid4())[1:7]
        group.code = unique_code
        group.admins = user
        group.members = user
        # print (group.get_data)
        _id = self.group_controller.insert(group)

        user_group = session.user.groups

        user_group_append = {
            'code': unique_code,
            'group_name': group_name
        }
    
        # user_group_list.append(str(_id)) # hex encoded ObjectId https://github.com/ankhers/mongodb/issues/40
        # print('inserted_id: '  + str(_id))
        # user_group_list.append(group_name)
        user_group.append(user_group_append)
        # self.user_repository.pushGroup(session.user.username, bson.BSON.encode(group))

        self.user_controller.insert(session.user)

        session.send({
            'To': 'group create',
            'status': 'Success',
            'message': 'Group has been created'
        })

    def __join_group(self, session: Session, request):
        request_code = request['code']
        group = self.group_controller.get_code(request_code)
        if group is not None:
            print(group)
            print('code: ' + group.code)
            group_name = group.name
            group_code = group.code

            members = group.members
            username = session.user.username
            if username not in members:
                members.append(username)
            self.group_controller.insert(group)

            user_group = session.user.groups
            user_group_append = {
                'code': group_code,
                'group_name': group_name
            }
            user_group.append(user_group_append)
            self.user_controller.insert(session.user)

            session.send({
                'To': 'group join',
                'status': 'Success',
                'message': 'You have joined this group'
            })

        else:
            session.send({
                'To': 'group join',
                'status': 'ERROR',
                'message': 'Group code is invalid'
            })

    def __exit_group(self, session: Session, request):
        request_code = request['code']
        group = self.group_controller.get_code(request_code)
        if group is not None:
            group_members = group.members
            username = session.user.username
            if username in group_members:
                group_members.remove(username)
                self.group_controller.insert(group)

                user_group = session.user.groups
                for i in range(len(user_group)):
                    if user_group[i]['code'] == request_code:
                        del user_group[i]
                        break

                self.user_controller.insert(session.user)

                session.send({
                    'To': 'group exit',
                    'status': 'Success',
                    'message': 'You have left this group'
                })
            else:
                session.send({
                    'To': 'group exit',
                    'status': 'ERROR',
                    'message': 'You are not belong to this group'
                })
        else:
            session.send({
                'FOR': 'group exit',
                'status': 'ERROR',
                'message': 'Group is not available'
            })

