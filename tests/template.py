
# --- QUICK AND DIRTY ---
import sys, os

dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(dir)
os.chdir(parent_dir)
sys.path.append(parent_dir)
# -----------------------

from telegram_bot import TelegramBot

# insert own bot-token here
token = ""

bot = TelegramBot(bot_token_= token)


while True:
    result = bot.poll()

    # do something
