from . import telegram_bot as tb

# insert own bot-token here
token = ""

bot = tb.TelegramBot(bot_token_= token)


while True:
    result = bot.poll()

    # do something
