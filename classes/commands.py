# classes for commands

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
