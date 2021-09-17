# Brain4Tech Python Telegram Bot
*A simple and lightweight Python Telegram Bot with a small range of functionalities using the [Telegram Bot API](https://core.telegram.org/bots/api)*

**Requirements:**

1. The latest [Python](https://www.python.org/downloads/) version with following libraries:
	 - [requests](https://pypi.org/project/requests/) (`pip install requests`)
2. A bot token from [BotFather](https://core.telegram.org/bots#6-botfather)


**Currently supported:**

 - sending and receiving messages, images, audio, video and documents
 - polls
 - inline- and keyboardbuttons
 - callback-queries
 - bot-commands
 - "single-chat mode": bot is only active in one single chat/group/channel
 - new chat members


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

    bot = TelegramBot ("<insert bot_token here>")
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

Check the Update-class in classes/updates.py for more. It's pretty self explaining.


**Good-to-know:**

 - the codebase is still in development. Bugs can occur, features are not fully implemented, and so on..
 - this repository is NOT a pip-package (yet). You need to download this repository as a *.zip-file (and extract it afterwards) in order to use it in your own project
 - I added a directory called "tests" with a template-script. You can use that to get started as well.
 - Mistakes and Bugs ~~*can*~~ *will* occur! If you found one, please open an issue :)
 - This code is **FREE** to use! YEYY!


**About Me:**

 - software-engineering student from Germany (3rd semester)
 - 2/3 years of Python experience
 - I've been studying the Telegram Bot API for 1 1/2 years and released small scripts in [my other repository](https://github.com/brain4tech/telegram-bot-api-scripts). But that coding style is unusable for bigger projects so I decided to create an own little library for future projects and other people who want to learn the Telegram Bot API without going through the pain I've been going through.
 - beginner at GitHub and publishing code.
 - English is obviously **not** my first language


Feel free to make a pull request and help me making this repository beginner- and user-friendly!
