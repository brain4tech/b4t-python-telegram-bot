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
    def __init__(self, button_type_: type, button_list_: list = []):

        self.button_type = None
        self.button_type_str = ""
        self.__button_list = []

        if button_type_ == InlineButton:
            self.button_type = button_type_
            self.button_type_str = "inline"
        elif button_type_ == KeyboardButton:
            self.button_type = button_type_
            self.button_type_str = "keyboard"
        else:
            raise TypeError("given button_type is not type InlineButton or KeyboardButton")

        if button_list_:
            for element in button_list_:
                if isinstance(element, self.button_type):
                    self.button_list.append(element)


    def __str__(self):
        return str(self.toDict())

    def toDict(self):
        return [button.toDict() for button in self.list]

    def addCommand(self, button_):
        if isinstance(button_, self.button_type):
            self.button_list.append(button_)
    
    def bulkAddCommands (self, button_list: list):
        for element in button_list:
            if isinstance(element, self.button_type):
                self.button_list.append(element)
