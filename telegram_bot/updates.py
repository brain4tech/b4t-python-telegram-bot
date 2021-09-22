# general class for receiving updates

from .messages import Message, ChannelPost, Message, MessageEntity
from .misc import CallbackQuery
from .polls import Poll, PollAnswer


class Update:
    def __init__(self, data_: dict):
        self.content = data_
        self.id = data_['update_id']
        self.message = Message(
            data_['message']) if 'message' in data_ else None
        self.channel_post = ChannelPost(
            data_['channel_post']) if 'channel_post' in data_ else None
        self.callback = CallbackQuery(
            data_['callback_query']) if 'callback_query' in data_ else None
        self.poll = Poll(data_['poll']) if 'poll' in data_ else None
        self.poll_answer = PollAnswer(
            data_['poll_answer']) if 'poll_answer' in data_ else None

    def isMessage(self):
        return True if self.message else False

    def isChannelPost(self):
        return True if self.channel_post else False

    def isPhoto(self):
        try:
            return True if self.message.photo else False
        except Exception:
            return False

    def isVideo(self):
        try:
            return True if self.message.video else False
        except Exception:
            return False

    def isAudio(self):
        try:
            return True if self.message.audio else False
        except Exception:
            return False

    def isDocument(self):
        try:
            return True if self.message.document else False
        except Exception:
            return False

    def isPoll(self):
        return True if self.poll else False

    def isPollAnswer(self):
        return True if self.poll_answer else False

    def isnewChatMember(self):
        try:
            return True if self.message.new_chat_members else False
        except Exception:
            return False

    def isCallback(self):
        return True if self.callback else False

    def isBotCommand(self):
        try:
            for entity in self.message.entities.list:
                if isinstance(entity, MessageEntity):
                    if entity.type == "bot_command":
                        return entity
        except Exception:
            return False
