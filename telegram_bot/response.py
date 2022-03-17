# class for reponse of Telegram API

from .messages import Message

class TelegramResponse:
    def __init__(self, data: dict, bypass_message_object_decoding = False):
        self.ok = data['ok']
        self.code = None
        self.description = None
        self.result = None

        if self.ok:
            if isinstance(data['result'], dict) and not bypass_message_object_decoding:
                self.result = Message(data['result'])
            self.result = data['result']
        else:
            self.code = data['error_code']
            self.description = data['description']

    def isError(self):
        return not self.ok