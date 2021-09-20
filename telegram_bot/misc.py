# miscellanious classes

from .messages import Message, User


class CallbackQuery:
    def __init__(self, data_: dict):
        self.id = data_['id']
        self.sender = User(data_['from'])
        self.message = Message(data_['message'])
        self.data = data_['data']
