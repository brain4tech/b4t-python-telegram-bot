# classes for inline and reply keyboards

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
