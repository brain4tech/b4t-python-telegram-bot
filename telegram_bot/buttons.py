# classes for inline and reply keyboards

class InlineButton:
    def __init__(self, text_, callback_data_, url_=""):
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

        self.__button_type = None
        self.__button_type_str = ""
        self.__button_list = []

        if button_type_ == InlineButton:
            self.__button_type = button_type_
            self.__button_type_str = "inline"
        elif button_type_ == KeyboardButton:
            self.__button_type = button_type_
            self.__button_type_str = "keyboard"
        else:
            raise TypeError(
                "given button_type is not type InlineButton or KeyboardButton")

        if button_list_:
            for element in button_list_:
                if isinstance(element, self.__button_type):
                    self.__button_list.append(element)

    def __str__(self):
        return str(self.toDict())

    def toDict(self):
        return [button.toDict() for button in self.__button_list]

    def addCommand(self, button_):
        if isinstance(button_, self.__button_type):
            self.__button_list.append(button_)

    def bulkAddCommands(self, button_list: list):
        for element in button_list:
            if isinstance(element, self.__button_type):
                self.__button_list.append(element)

    def getButtonType(self):
        return self.__button_type

    def toBotDict(self, special_button: type = None, column_count: int = 3):

        button_list = []
        button_row = []

        for button in self.__button_list:
            button_row.append(button.toDict())

            if len(button_row) >= column_count or button == self.__button_list[-1]:
                button_list.append(button_row[:])
                button_row.clear()

        if special_button and isinstance(special_button, self.__button_type):
            button_list.append([special_button.toDict()])

        return {f'{"inline_" if self.__button_type_str == "inline" else ""}keyboard': button_list}
