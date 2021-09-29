# simple and lightweight telegram bot using the Telegram Bot API
# https://core.telegram.org/bots/api

from .updates import Update
from .commands import BotCommandList
from .chatmembers import ChatMember

import json
import requests


class TelegramBot:
    def __init__(self, bot_token_, return_on_update_only: bool = True, single_chat_mode_ = False):
        if not bot_token_:
            raise ValueError("Passed bot-token is empty.")
        
        self.__token = str(bot_token_).strip().replace(' ', '')

        # check with /me if token is valid

        if not self.__token:
            raise ValueError("Given token is not valid.")

        # if bot should only work for one specific chat (other chats will be ignored).
        # single_chat_mode_ needs to be the correct chat-id in order for this functionality to be activated
        self.__single_chat_mode = int(single_chat_mode_)
        self.__return_on_update_only = bool(return_on_update_only)

        self.__base_url = f"https://api.telegram.org/bot{self.__token}"
        self.__offset = 0

        response = requests.get(self.__base_url + "/getMe").json()
        if not response['ok']:
            raise ValueError(f"Passed token not accepted by Telegram. Please check and try again: {response['description']}")

    def poll(self):
        while True:
            try:
                update = requests.get(self.__base_url + "/getUpdates", data={'offset': self.__offset}).json()

                if update['ok'] and update['result']:
                    result = Update(update['result'][0])
                else:
                    result = False

                if result:
                    self.__setOffset(result.id + 1)

                    if self.__single_chat_mode:
                        try:
                            if result.isMessage() and result.message.chat.id == self.__single_chat_mode:
                                return result, update

                            if result.isCallback() and result.callback.message.chat.id == self.__single_chat_mode:
                                return result, update

                        except Exception as e:
                            print(
                                f"An error occurred while checking conditions: {e}")

                    else:
                        return result, update
                
                elif not self.__return_on_update_only:
                    return result, update

            except Exception as e:
                print(f"An error occurred: {repr(e)}")

    def sendMessage(self, chat_id, message, keyboard: dict = None):

        data = {
            'chat_id': chat_id,
            'text': message,
            'reply_markup': json.dumps(keyboard) if keyboard else ""
        }

        return requests.post(self.__base_url + "/sendMessage", data=data)

    def sendPhoto(self, chat_id, photo_path, caption=""):

        data = {
            'chat_id': chat_id,
            'caption': caption
        }

        photo = {'photo': open(photo_path, 'rb')}

        return requests.post(self.__base_url + "/sendPhoto", data=data, files=photo)

    def sendVideo(self, chat_id, video_path, caption="", duration: int = 0, width: int = 0, height: int = 0, thumbnail_path=""):
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

        return requests.post(self.__base_url + "/sendVideo", data=data, files=media)

    def sendAudio(self, chat_id, audio_path, caption="", length: int = 0, performer: str = "", title: str = "", thumbnail_path=""):
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

        return requests.post(self.__base_url + "/sendAudio", data=data, files=media)

    def sendDocument(self, chat_id, document_path, caption="", thumbnail_path=""):
        data = {
            'chat_id': chat_id,
            'caption': caption
        }

        media = {'photo': open(document_path, 'rb')}

        if thumbnail_path:
            media['thumb'] = open(thumbnail_path, 'rb')

        return requests.post(self.__base_url + "/sendDocument", data=data, files=media)

    def sendPoll(self, chat_id: int, question: str, options: list, is_anonymous: bool = True, poll_type: str = "regular",
                 multiple_answers: bool = False, correct_option: int = 0, explanation: str = "", open_period: int = 0, close_date: int = None):

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

        return requests.post(self.__base_url + "/sendPoll", data=data)

    def __setOffset(self, offset: int):
        self.__offset = offset

    # USE WITH CAUTION!
    def increaseOffset(self):
        self.__offset += 1

    def editMessage(self, chat_id, message_id, text, keyboard: dict = None):

        # you can only edit messages which do not have a reply-keyboard

        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text,
            'reply_markup': json.dumps(keyboard) if keyboard else ""
        }
    
        return requests.post(self.__base_url + "/editMessageText", data=data)
    
    def editMessageInlineKeyboard(self, chat_id, message_id, keyboard: dict):

        # you can only edit messages which do not have a reply-keyboard

        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'reply_markup': json.dumps(keyboard)
        }

        return requests.post(self.__base_url + "/editMessageReplyMarkup", data=data)

    def deleteMessage(self, chat_id, message_id):
        data = {
            'chat_id': chat_id,
            'message_id': message_id
        }

        return requests.post(self.__base_url + "/deleteMessage", data=data)

    def answerCallbackQuery(self, query_id, text):
        data = {
            'callback_query_id': query_id,
            'text': text
        }

        return requests.post(self.__base_url + "/answerCallbackQuery", data=data)

    def setBotCommands(self, command_list: BotCommandList):
        if isinstance(command_list, BotCommandList):
            data = {'commands': json.dumps(command_list.toDict())}

            return requests.post(self.__base_url + "/setMyCommands", data=data)
        else:
            raise TypeError(f"command_list ist type {type(command_list)} and not BotCommmandList")

    def deleteBotCommands(self):
        return requests.post(self.__base_url + "/deleteMyCommands")

    def getBotCommands(self):
        return requests.get(self.__base_url + "/getMyCommands").json()

        # convert json to package-own command-classes?
    
    def banChatMember(self, chat_id, user_id):
        data = {
            'chat_id': chat_id,
            'user_id': user_id
        }

        return requests.post(self.__base_url + "/banChatMember", data=data)

    def unbanChatMember(self, chat_id, user_id, only_if_banned = True):
        data = {
            'chat_id': chat_id,
            'user_id': user_id,
            'only_if_banned': bool(only_if_banned)
        }

        return requests.post(self.__base_url + "/unbanChatMember", data=data)
    
    def kickChatMember (self, chat_id, user_id):
        return self.unbanChatMember(chat_id, user_id, False)
    
    def getChatMember (self, chat_id, user_id):
        data = {
            'chat_id': chat_id,
            'user_id': user_id
        }

        response = requests.post(self.__base_url + "/getChatMember", data=data)
        try:
            if response['ok'] and response['result']:
                return ChatMember(response['result'])
            else:
                return None
        except Exception:
            return None

    
    def getChatAdministrators(self, chat_id):

        data = {
            'chat_id': chat_id
        }

        response = requests.post(self.__base_url + "/getChatAdministrators", data=data)

        try:
            if response['ok'] and response['result']:
                return [ChatMember(member) for member in response['result']]
        except Exception:
            return None

