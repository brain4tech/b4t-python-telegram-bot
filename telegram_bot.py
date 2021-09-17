# simple and lightweight telegram bot using the Telegram Bot API
# https://core.telegram.org/bots/api

import json
import requests

class TelegramBot:
    def __init__(self, bot_token_, single_chat_mode_ = False):
        self.__token = bot_token_
        
        # if bot should only work for one specific chat (other chats will be ignored).
        # single_chat_mode_ needs to be the correct chat-id in order for this functionality to be activated
        self.__single_chat_mode = int(single_chat_mode_)

        self.__base_url = f"https://api.telegram.org/bot{self.__token}"
        self.__offset = 0
    
    def poll(self):
        while True:
            try:
                update = requests.get(self.__base_url + "/getUpdates", data = {'offset': self.__offset}).json()
                
                if update['ok'] and update['result']: result = Update(update['result'][0])
                else: result = False

                if result:
                    self.__setOffset(result.id + 1)

                    if self.__single_chat_mode:
                        try:
                            if result.isMessage() and result.message.chat.id == self.__single_chat_mode:
                                return result

                            if result.isCallback() and result.callback.message.chat.id == self.__single_chat_mode:
                                    return result
                            
                        except Exception as e:
                            print (f"An error occurred while checking conditions: {e}")
                    
                    else:
                        return result

            except Exception as e:
                print (f"An error occurred: {repr(e)}")

    def sendMessage(self, chat_id, message, keyboard:dict = None):
        if not keyboard:
            reply_markup = json.dumps({'remove_keyboard': True})
        else:
            keyboard['resize_keyboard'] = True
            keyboard['one_time_keyboard'] = True
            reply_markup = json.dumps(keyboard)
        
        data = {
            'chat_id': chat_id,
            'text': message,
            'reply_markup': reply_markup
            }   

        requests.post(self.__base_url + "/sendMessage", data=data)

    def sendPhoto(self, chat_id, photo_path, caption = ""):

        data = {
            'chat_id': chat_id,
            'caption': caption
            }

        photo = {'photo': open(photo_path, 'rb')}

        requests.post(self.__base_url + "/sendPhoto", data=data, files=photo)
    
    def sendVideo(self, chat_id, video_path, caption = "", duration: int = 0, width: int = 0, height: int = 0, thumbnail_path = ""):
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'duration': duration if duration else None,
            'width': width if width else None,
            'height': height if height else None
            }

        media = {'photo': open(video_path, 'rb')}
        
        if thumbnail_path:
            media['thumb'] = open(thumbnail_path, 'rb')

        requests.post(self.__base_url + "/sendVideo", data=data, files=media)


    def sendAudio(self, chat_id, audio_path, caption = "", length: int = 0, performer: str = "", title: str = "", thumbnail_path = ""):
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'length': length if length else None,
            'performer': performer,
            'title': title,
            }
    
        media = {'photo': open(audio_path, 'rb')}
        
        if thumbnail_path:
            media['thumb'] = open(thumbnail_path, 'rb')

        requests.post(self.__base_url + "/sendAudio", data=data, files=media)


    def sendDocument(self, chat_id, document_path, caption = "", thumbnail_path = ""):
        data = {
            'chat_id': chat_id,
            'caption': caption
            }

        media = {'photo': open(document_path, 'rb')}
        
        if thumbnail_path:
            media['thumb'] = open(thumbnail_path, 'rb')

        requests.post(self.__base_url + "/sendDocument", data=data, files=media)
    
    def sendPoll (self, chat_id: int, question: str, options: list, is_anonymous: bool = True, poll_type: str = "regular",
                multiple_answers: bool = False, correct_option:int = 0, explanation: str = "", open_period: int = 0, close_date: int = None):

        data = {
            'chat_id': chat_id,
            'question': question,
            'options': json.dumps(options),
            'is_anonymous': is_anonymous,
            'type': poll_type if poll_type == "regular" or poll_type == "quiz" else "regular",
            'allows_multiple_answers': bool(multiple_answers) if poll_type == "regular" else False,
            'correct_option_id': int(correct_option) if poll_type == "quiz" else 0,
            'explanation': str(explanation) if poll_type == "quiz" else "",
            'open_period': open_period if open_period >= 5 and open_period <= 600 else None
            # TODO: closed_date
            }
        
        if open_period > 5:
            data['open_period'] = open_period

        requests.post(self.__base_url + "/sendPoll", data=data)


    def __setOffset(self, offset: int):
        self.__offset = offset

    # USE WITH CAUTION!
    def increaseOffset (self):
        self.__offset += 1
    
    def editMessage (self, chat_id, message_id, text, inline_keyboard:dict = None):
        if not inline_keyboard:
            reply_markup = json.dumps({'remove_keyboard': True})
        else:
            inline_keyboard['resize_keyboard'] = True
            inline_keyboard['one_time_keyboard'] = True
            reply_markup = json.dumps(inline_keyboard)
        
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text,
            'reply_markup': reply_markup
        }

        requests.post(self.__base_url + "/editMessageText", data = data)
    
    def deleteMessage (self, chat_id, message_id):
        data = {
            'chat_id': chat_id,
            'message_id': message_id
            }

        requests.post(self.__base_url + "/deleteMessage", data=data)
    
    def answerCallbackQuery (self, query_id, text):
        data = {
                'callback_query_id': query_id,
                'text': text
                }

        requests.post(self.__base_url + "/answerCallbackQuery", data=data)

    def setBotCommands(self, command_list):
        if isinstance(command_list, BotCommandList):
            data = {'commands': json.dumps(command_list.toDict())}
            
            requests.post(self.__base_url + "/setMyCommands", data=data)
    
    def deleteBotCommands(self):
        requests.post(self.__base_url + "/deleteMyCommands")
    
    def getBotCommands(self):
        return requests.get(self.__base_url + "/getMyCommands").json()


    @staticmethod
    # requires 2d-Array with each button : [[text shown in button, callback data, <MORE TO COME!>]]
    def listToKeyboard(items, special_button=False, column_count: int = 3):
        button_send = []
        button_row = []

        for item in items:
            button_row.append({'text': str(item[1]), 'callback_data': str(item[0])})

            if len(button_row) >= column_count or item == items[-1]:
                button_send.append(button_row[:])
                button_row.clear()

        if special_button:
            button_send.append([{'text': str(special_button), 'callback_data': 'special_button'}])

        return button_send
    
    @staticmethod
    def keyboardListToKeyboard (keyboard_list, special_button = False, column_count: int = 3):
        if isinstance(keyboard_list, ButtonList):
            button_send = []
            button_row = []

            for item in keyboard_list.list:
                button_row.append(item.toDict())

                if len(button_row) >= column_count or item == keyboard_list.list[-1]:
                    button_send.append(button_row[:])
                    button_row.clear()

            if special_button and isinstance(special_button, InlineButton or KeyboardButton):
                button_send.append([special_button.toDict()])

            return button_send

        return False


# classes returning incoming json as an object
class User:
    def __init__(self, data_: dict):
        self.id = data_['id']
        self.first_name = data_['first_name']
        self.last_name = data_['last_name'] if 'last_name' in data_ else ""
        self.username = data_['username'] if 'username' in data_ else ""
    
class Chat:
    def __init__(self, data_: dict):
        self.id = data_['id']
        self.type = data_['type']
        self.title = data_['title'] if 'title' in data_ else ""
    
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

class Message:
    def __init__(self, data_: dict):
        self.id = data_['message_id']
        self.sender = User(data_['from'])
        self.chat = Chat(data_['chat'])
        self.date = data_['date']
        self.text = data_['text']
        self.entities = MessageEntityList(data_['entities']) if 'entities' in data_ else None
        self.photo = [Photo(photo) for photo in data_['photo']] if 'photo' in data_ else None
        self.video = Video(data_['video']) if 'video' in data_ else None
        self.audio = Audio(data_['audio']) if 'audio' in data_ else None
        self.document = Document(data_['document']) if 'document' in data_ else None
        self.new_chat_members = [User(user) for user in data_['new_chat_members']] if 'new_chat_members' in data_ else None

class ChannelPost(Message):
    pass

class Photo:
    def __init__(self, data_: dict):
        self.file_id = data_['file_id']
        self.file_unique_id = data_['file_unique_id']
        self.width = data_['width']
        self.height = data_['height']
        self.size = data_['size'] if 'size' in data_ else None

class Video:
    def __init__(self, data_: dict):
        self.file_id = data_['file_id']
        self.file_unique_id = data_['file_unique_id']
        self.width = data_['width']
        self.height = data_['height']
        self.length = data_['length']
        self.thumb = Photo(data_['thumb']) if 'thumb' in data_ else None
        self.file_name = data_['file_name'] if 'file_name' in data_ else None
        self.file_size = data_['file_size'] if 'file_size' in data_ else None

class Audio:
    def __init__(self, data_: dict):
        self.file_id = data_['file_id']
        self.file_unique_id = data_['file_unique_id']
        self.duration = data_['duration']
        self.performer = data_['performer'] if 'performer' in data_ else None
        self.title = data_['title'] if 'title' in data_ else None
        self.file_name = data_['file_name'] if 'file_name' in data_ else None
        self.file_size = data_['file_size'] if 'file_size' in data_ else None
        self.thumb = Photo(data_['thumb']) if 'thumb' in data_ else None

class Document:
    def __init__(self, data_: dict):
        self.file_id = data_['file_id']
        self.file_unique_id = data_['file_unique_id']
        self.thumb = Photo(data_['thumb']) if 'thumb' in data_ else None
        self.file_name = data_['file_name'] if 'file_name' in data_ else None
        self.file_size = data_['file_size'] if 'file_size' in data_ else None


class Poll:
    def __init__(self, data_: dict):
        self.id = data_['id']
        self.question = data_['question']
        self.options = [PollOption(option) for option in data_['options']]
        self.total_voter_count = data_['total_voter_count']
        self.is_closed = data_['is_closed']
        self.is_anonymous = data_['is_anonymous']
        self.type = data_['type']
        self.allows_multiple_answers = data_['allows_multiple_answers']
        self.correct_option_id = data_['correct_option_id'] if 'correct_option_id' in data_ else None
        self.explanation = data_['explanation'] if 'explanation' in data_ else None
        self.open_period = data_['open_period'] if 'open_period' in data_ else None
        self.closed_data = data_['closed_data'] if 'closed_data' in data_ else None

class PollOption:
    def __init__(self, data_: dict):
        self.text = data_['text']
        self.voter_count = data_['voter_count']

class PollAnswer:
    def __init__(self, data_: dict):
        self.poll_id = data_['poll_id']
        self.user = User(data_['user'])
        self.options_ids = data_['option_ids']

class CallbackQuery:
    def __init__(self, data_: dict):
        self.id = data_['id']
        self.sender = User(data_['from'])
        self.message = Message(data_['message'])
        self.data = data_['data']
    
class BotCommand:
    def __init__(self, command_: str, description_: str):
        self.command = command_
        self.description = description_
    
    def __str__(self):
        return str(self.toDict())
    
    def toDict(self):
        return self.__dict__

class BotCommandList:
    def __init__(self, command_list: list = None):
        self.list = []

        if command_list:
            for element in command_list:
                if isinstance(element, BotCommand):
                    self.list.append(element)
        
    def __str__(self):
        return str(self.toDict())

    def toDict(self):
        return [command.toDict() for command in self.list]

    def addCommand(self, command_: BotCommand):
        self.list.append(command_)
    
    def bulkAddCommands (self, command_list: list):
        for element in command_list:
            if isinstance(element, BotCommand):
                self.list.append(element)

class InlineButton:
    def __init__(self, text_, callback_data_, url_ = ""):
        self.text = text_
        self.callback_data = callback_data_
        self.url = url_
    
    def __str__(self):
        return str(self.toDict())
    
    def toDict(self):
        return self.__dict__

class KeyboardButton:
    def __init__(self, text_):
        self.text = text_

    def __str__(self):
        return str(self.toDict())
    
    def toDict(self):
        return self.__dict__


class ButtonList:
    def __init__(self, instance_type: type, button_list: list = []):

        if instance_type == InlineButton or instance_type == KeyboardButton:

            self.list = []

            if button_list:
                for element in button_list:
                    if isinstance(element, instance_type):
                        self.list.append(element)
        
        else:
            raise TypeError("instance_type is not type InlineButton or keyboardButton")
    
    def __str__(self):
        return str(self.toDict())

    def toDict(self):
        return [button.toDict() for button in self.list]

    def addCommand(self, button_: InlineButton):
        self.list.append(button_)
    
    def bulkAddCommands (self, command_list: list):
        for element in command_list:
            if isinstance(element, InlineButton):
                self.list.append(element)

class Update:
    def __init__(self, data_: dict):
        self.content = data_
        self.id = data_['update_id']
        self.message = Message(data_['message']) if 'message' in data_ else None
        self.channel_post = ChannelPost(data_['channel_post']) if 'channel_post' in data_ else None
        self.callback = CallbackQuery(data_['callback_query']) if 'callback_query' in data_ else None
        self.poll = Poll(data_['poll']) if 'poll' in data_ else None
        self.poll_answer = PollAnswer(data_['poll_answer']) if 'poll_answer' in data_ else None
        

    def isMessage (self):
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
    
    def isnewChatMember (self):
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
                    if entity.type == "bot_command": return entity
        except Exception:
            return False

if __name__ == '__main__':
    
    # insert own bot-token here
    token = ""

    bot = TelegramBot(bot_token_= token)


    while True:
        result = bot.poll()

        # do something
    