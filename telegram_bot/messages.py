# classes for messages in updates

from .media import Photo, Video, Audio, Document


class Message:
    def __init__(self, data_: dict):
        self.id = data_['message_id']
        self.sender = User(data_['from'])
        self.chat = Chat(data_['chat'])
        self.date = data_['date']
        self.text = data_['text'] if 'text' in data_ else None
        self.entities = MessageEntityList(
            data_['entities']) if 'entities' in data_ else None
        self.photo = [Photo(photo) for photo in data_[
            'photo']] if 'photo' in data_ else None
        self.video = Video(data_['video']) if 'video' in data_ else None
        self.audio = Audio(data_['audio']) if 'audio' in data_ else None
        self.document = Document(
            data_['document']) if 'document' in data_ else None
        self.new_chat_members = [User(user) for user in data_[
            'new_chat_members']] if 'new_chat_members' in data_ else None


class ChannelPost(Message):
    pass


class MessageEntity:
    def __init__(self, data_: dict):
        self.type = data_['type']
        self.offset = data_['offset']
        self.length = data_['length']


class MessageEntityList:
    def __init__(self, data_: dict):
        self.list = []

        for element in data_:
            try:
                self.list.append(MessageEntity(element))
            except Exception as e:
                pass


class User:
    def __init__(self, data_: dict):
        self.id = data_['id']
        self.first_name = data_['first_name']
        self.last_name = data_['last_name'] if 'last_name' in data_ else ""
        self.username = data_['username'] if 'username' in data_ else ""
    
    def __str__(self):
        return str(self.toDict())
    
    def toDict(self):
        return self.__dict__


class Chat:
    def __init__(self, data_: dict):
        self.id = data_['id']
        self.type = data_['type']
        self.title = data_['title'] if 'title' in data_ else ""
