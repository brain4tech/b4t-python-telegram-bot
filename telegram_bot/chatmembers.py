# (base)classes for chat members

from .messages import User

class ChatMember:
    def __init__(self, data_: dict):
        self.status = data_['status']
        self.user = User(data_['user'])

    def __str__(self):
        return str(self.toDict())

    def toDict(self):
        return {'status': self.status, 'user': self.user.toDict()}