# __init__.py

# version of package
__version__ = "1.0.0"

# importing all classes
from .bot import TelegramBot
from .buttons import KeyboardButton, InlineButton, ButtonList
from .chatmembers import ChatMember
from .chatpermissions import ChatPermissions
from .commands import BotCommand, BotCommandList
from .media import PhotoSize, Video, Animation, Audio, Document
from .messages import Message, ChannelPost, MessageEntity, MessageEntityList, User, Chat
from .misc import CallbackQuery
from .polls import Poll, PollOption, PollAnswer
from .updates import Update
from .dice import Dice
from .contact import Contact
from .location import Location, Venue
from .chataction import ChatAction
from .inputmedia import InputMedia, InputMediaPhoto, InputMediaVideo, InputMediaAnimation, InputMediaAudio, InputMediaDocument, InputMediaList
from .response import TelegramResponse
