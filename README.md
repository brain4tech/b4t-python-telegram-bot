# Brain4Tech Python Telegram Bot
*A simple and lightweight Python Telegram Bot with a small range of functionalities using the [Telegram Bot API](https://core.telegram.org/bots/api)*

Installation with pip: `pip install b4t-python-telegram-bot`

**Requirements:**

1. the latest [Python](https://www.python.org/downloads/) version with following libraries:
	 - [requests](https://pypi.org/project/requests/) (`pip install requests`)
2. a bot token from [BotFather](https://core.telegram.org/bots#6-botfather)


**Currently supported:**

 - sending and receiving messages, images, audio, video and documents
 - polls
 - inline- and keyboardbuttons
 - callback-queries
 - bot-commands
 - "single-chat mode": bot is only active in one single chat/group/channel
 - "return-on-update-only mode": bot only returns a value when it receives a valid update
 - new chat members
 - ban, unban or kick members from group-like chats


**Future plans:**

 - download images, audio, video and documents
 - add more media and interactable features (like voice, dices, media groups, locations and contacts)
 - proper method for turning keyboards to a json-string
 - get chat information and set chat attributes (like chat photo and description)
 - forward messages
 - improve "single-chat mode"
 - add time delay between requests and use timeout features
 - propper documentation


**How it works:**

The bot frequently sends a request to the telegram server and gets a response. If there is usable content within the response (i.e. someone send a message to the bot or into a group where the bot is a group member of) it parses the response into a custom datastructure ( = classes, lol) which the programmer gets in return to work with. The structure of the returned class is the same as Telegram sends the response, which means you can get your needed information like you can see [here](https://core.telegram.org/bots/api#update).
*Example:* I want to know what the content is of the message I just received:

    from telegram_bot import TelegramBot
    bot = TelegramBot ("<insert your bot_token here>")
    response = bot.poll()
    
    if response:    
	    message = response.message.text

Easy! You can also check if your response is a message or (for example) an incoming command or a callback from an inline-keyboard:

    [see above]
    
    if response:    
	    if response.isMessage():
		    # do stuff here
		elif response.isCallback():
			# do other stuff here
		elif response.isBotCommand():
			# you know what's coming...

Check the Update-class in telegram_bot/updates.py for more. It's pretty self explaining.


**Good-to-know:**

 - the codebase is still in development.
 - Mistakes and Bugs ~~*can*~~ *will* occur! If you found one, please open an issue :)
 - This code is **FREE** to use! YEYY!


**About Me:**

 - software-engineering student from Germany (3rd semester)
 - 2-3 years of Python experience
 - I've been studying the Telegram Bot API for 1 1/2 years and released small scripts in [my other repository](https://github.com/brain4tech/telegram-bot-api-scripts). Unfortunately that coding style is unusable for bigger projects so I decided to create an own little library for future projects and other people who want to learn the Telegram Bot API without going through the pain I've been going through.
 - beginner at GitHub and publishing code.
 - English is obviously **not** my first language


Feel free to make a pull request and help me making this repository beginner- and userfriendly!
