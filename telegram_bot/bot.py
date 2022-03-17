# simple and lightweight telegram bot using the Telegram Bot API
# https://core.telegram.org/bots/api

from .updates import Update
from .response import TelegramResponse
from .commands import BotCommand, BotCommandList
from .chatmembers import ChatMember
from .chatpermissions import ChatPermissions
from .dice import Dice
from .inputmedia import InputMediaList

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
            # TODO get own id so bot cannot ban or restrict itself

            raise ValueError(f"Passed token not accepted by Telegram. Please check and try again: {response['description']}")

    def poll(self, one_time = False):

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
                
                if one_time:
                    return result, update
                
                elif not self.__return_on_update_only:
                    return result, update

            except Exception as e:
                print(f"An error occurred: {repr(e)}")
    
    def __setOffset(self, offset: int):
        self.__offset = offset

    # USE WITH CAUTION!
    def increaseOffset(self):
        self.__offset += 1

    def sendMessage(self, chat_id, message, keyboard: dict = None, markdown_style = False, silent = False):

        data = {
            'chat_id': chat_id,
            'text': message,
            'disable_notification': bool(silent),
            'reply_markup': json.dumps(keyboard) if keyboard else "",
            'parse_mode': "MarkdownV2" if markdown_style else ""
        }

        response_raw = requests.post(self.__base_url + "/sendMessage", data=data).json()
        return TelegramResponse(response_raw), response_raw

    def sendPhoto(self, chat_id, photo_path, caption="", markdown_style = False, silent = False):

        data = {
            'chat_id': chat_id,
            'caption': caption,
            'disable_notification': bool(silent),
            'parse_mode': "MarkdownV2" if markdown_style else None
        }

        photo = {'photo': open(photo_path, 'rb')}

        response_raw = requests.post(self.__base_url + "/sendPhoto", data=data, files=photo).json()
        return TelegramResponse(response_raw), response_raw


    def sendVideo(self, chat_id, video_path, caption="", duration: int = 0, width: int = 0, height: int = 0, thumbnail_path="", markdown_style = False, silent = False):
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'duration': duration if duration else None,
            'width': width if width else None,
            'height': height if height else None,
            'disable_notification': bool(silent),
            'parse_mode': "MarkdownV2" if markdown_style else ""
        }

        media = {'video': open(video_path, 'rb')}

        if thumbnail_path:
            media['thumb'] = open(thumbnail_path, 'rb')

        response_raw = requests.post(self.__base_url + "/sendVideo", data=data, files=media).json()
        return TelegramResponse(response_raw), response_raw

    def sendAnimation(self, chat_id, animation_path, caption="", duration: int = 0, width: int = 0, height: int = 0, thumbnail_path="", markdown_style = False, silent = False):
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'duration': duration if duration else None,
            'width': width if width else None,
            'height': height if height else None,
            'disable_notification': bool(silent),
            'parse_mode': "MarkdownV2" if markdown_style else ""
        }

        media = {'animation': open(animation_path, 'rb')}

        if thumbnail_path:
            media['thumb'] = open(thumbnail_path, 'rb')

        response_raw = requests.post(self.__base_url + "/sendAnimation", data=data, files=media).json()
        return TelegramResponse(response_raw), response_raw


    def sendAudio(self, chat_id, audio_path, caption="", length: int = 0, performer: str = "", title: str = "", thumbnail_path="", markdown_style = False, silent = False):
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'length': length if length else None,
            'performer': performer,
            'title': title,
            'disable_notification': bool(silent),
            'parse_mode': "MarkdownV2" if markdown_style else ""
        }

        media = {'audio': open(audio_path, 'rb')}

        if thumbnail_path:
            media['thumb'] = open(thumbnail_path, 'rb')

        response_raw = requests.post(self.__base_url + "/sendAudio", data=data, files=media).json()
        return TelegramResponse(response_raw), response_raw

    def sendDocument(self, chat_id, document_path, caption="", thumbnail_path="", markdown_style = False, silent = False):
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'disable_notification': bool(silent),
            'parse_mode': "MarkdownV2" if markdown_style else ""
        }

        media = {'document': open(document_path, 'rb')}

        if thumbnail_path:
            media['thumb'] = open(thumbnail_path, 'rb')

        response_raw = requests.post(self.__base_url + "/sendDocument", data=data, files=media).json()
        return TelegramResponse(response_raw), response_raw

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

        response_raw = requests.post(self.__base_url + "/sendPoll", data=data).json()
        return TelegramResponse(response_raw), response_raw
    
    def sendDice(self, chat_id, emoji = Dice.DICE, silent = False):
        
        data = {
            'chat_id': chat_id,
            'emoji': emoji,
            'disable_notification': bool(silent),
        }

        response_raw = requests.post(self.__base_url + "/sendDice", data=data).json()
        return TelegramResponse(response_raw), response_raw

    def sendContact(self, chat_id, phone_number, first_name, last_name = "", vcard = "", silent = False):

        data = {
            'chat_id': chat_id,
            'phone_number': phone_number,
            'first_name': first_name,
            'last_name': last_name,
            'vcard': vcard,
            'disable_notification': bool(silent),
        }

        response_raw = requests.post(self.__base_url + "/sendContact", data=data).json()
        return TelegramResponse(response_raw), response_raw
    
    def sendLocation(self, chat_id, latitude, longitude, silent = False):

        data = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
            'disable_notification': bool(silent),
        }

        response_raw = requests.post(self.__base_url + "/sendLocation", data=data).json()
        return TelegramResponse(response_raw), response_raw

    def sendVenue(self, chat_id, latitude, longitude, title, address = 0, silent = False):

        data = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
            'title': title,
            'address': address,
            'disable_notification': bool(silent),
        }

        response_raw = requests.post(self.__base_url + "/sendVenue", data=data).json()
        return TelegramResponse(response_raw), response_raw
    
    def sendChatAction(self, chat_id, chat_action, silent = False):
        data = {
            'chat_id': chat_id,
            'action': chat_action,
            'disable_notification': bool(silent)
        }

        response_raw = requests.post(self.__base_url + "/sendChatAction", data=data).json()
        return TelegramResponse(response_raw), response_raw

    def sendMediaGroup(self, chat_id, media: InputMediaList, silent = False):
        media_data, media_media = media.toDict()
        
        data = {
            'chat_id': chat_id,
            'media': json.dumps(media_data),
            'disable_notification': bool(silent)
        }

        response_raw = requests.post(self.__base_url + "/sendMediaGroup", data=data, files=media_media).json()
        return TelegramResponse(response_raw), response_raw

    def editMessage(self, chat_id, message_id, text, keyboard: dict = None, markdown_style = False):

        # you can only edit messages which do not have a reply-keyboard

        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text,
            'reply_markup': json.dumps(keyboard) if keyboard else "",
            'parse_mode': "MarkdownV2" if markdown_style else ""
        }
    
        response_raw = requests.post(self.__base_url + "/editMessageText", data=data).json()
        return TelegramResponse(response_raw), response_raw
    
    def editMessageInlineKeyboard(self, chat_id, message_id, keyboard: dict):

        # you can only edit messages which do not have a reply-keyboard

        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'reply_markup': json.dumps(keyboard)
        }

        response_raw = requests.post(self.__base_url + "/editMessageReplyMarkup", data=data).json()
        return TelegramResponse(response_raw), response_raw

    def deleteMessage(self, chat_id, message_id):
        data = {
            'chat_id': chat_id,
            'message_id': message_id
        }

        response_raw = requests.post(self.__base_url + "/deleteMessage", data=data).json()
        return TelegramResponse(response_raw), response_raw

    def answerCallbackQuery(self, query_id, text):
        data = {
            'callback_query_id': query_id,
            'text': text
        }

        response_raw = requests.post(self.__base_url + "/answerCallbackQuery", data=data).json()
        return TelegramResponse(response_raw), response_raw

    def setBotCommands(self, command_list: BotCommandList):
        if isinstance(command_list, BotCommandList):
            data = {'commands': json.dumps(command_list.toDict())}

            response_raw = requests.post(self.__base_url + "/setMyCommands", data=data).json()
            return TelegramResponse(response_raw), response_raw
        else:
            raise TypeError(f"command_list ist type {type(command_list)} and not BotCommmandList")

    def deleteBotCommands(self):
        response_raw = requests.post(self.__base_url + "/deleteMyCommands").json()
        return TelegramResponse(response_raw), response_raw

    def getBotCommands(self):
        response_raw = requests.get(self.__base_url + "/getMyCommands").json()
        response = TelegramResponse(response_raw, True)

        if response.isError():
            response.result = None
        else:
            command_list = []
            for command in response.result:
                command_list.append(BotCommand(command['command'], command['description']))
            response.result = command_list

        return response, response_raw
    
    def banChatMember(self, chat_id, user_id):
        data = {
            'chat_id': chat_id,
            'user_id': user_id
        }

        response_raw = requests.post(self.__base_url + "/banChatMember", data=data).json()
        return TelegramResponse(response_raw), response_raw

    def unbanChatMember(self, chat_id, user_id, only_if_banned = True):
        data = {
            'chat_id': chat_id,
            'user_id': user_id,
            'only_if_banned': bool(only_if_banned)
        }

        response_raw = requests.post(self.__base_url + "/unbanChatMember", data=data).json()
        return TelegramResponse(response_raw), response_raw
    
    def kickChatMember (self, chat_id, user_id):
        response_ban = self.banChatMember(chat_id, user_id)
        response_unban = self.unbanChatMember(chat_id, user_id, True)

        return response_ban, response_unban
    
    def getChatMember (self, chat_id, user_id):
        data = {
            'chat_id': chat_id,
            'user_id': user_id
        }

        response_raw = requests.post(self.__base_url + "/getChatMember", data=data).json()
        response = TelegramResponse(response_raw, True)

        if response.isError():
            response.result = None
        else:
            response.result = ChatMember(response.result)

        return response, response_raw

    
    def getChatAdministrators(self, chat_id):

        data = {
            'chat_id': chat_id
        }

        response_raw = requests.post(self.__base_url + "/getChatAdministrators", data=data).json()
        response = TelegramResponse(response_raw, True)

        if response.isError():
            response.result = None
        else:
            response.result = [ChatMember(member) for member in response.result]

        return response, response_raw

    def restrictChatMember (self, chat_id, user_id, permissions: ChatPermissions):
        if not isinstance(permissions, ChatPermissions):
            raise ValueError(f"passed parameter 'permissions' must be type {type(ChatPermissions)}, not {type(permissions)}")
        
        data = {
            'chat_id': chat_id,
            'user_id': user_id,
            'permissions': json.dumps(permissions.toDict())
        }

        response_raw = requests.post(self.__base_url + "/restrictChatMember", data=data).json()
        return TelegramResponse(response_raw), response_raw


