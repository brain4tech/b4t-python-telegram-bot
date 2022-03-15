# classes for all sorts of input media

class InputMedia:
    def __init__(self, type, media_path, thumb_path = "", caption = ""):
        self.type = type
        self.media_path = media_path
        self.thumb_path = thumb_path
        self.caption = caption

    def toDict(self):
        data = {
            'type': self.type,
            'media': f'attach://{self.media_path}',
            'thumb': f'attach://{self.thumb_path}' if self.thumb_path else '',
            'caption': self.caption if self.caption else ''
        }

        media = {f'{self.media_path}': open(self.media_path, 'rb')}
        if self.thumb_path:
            media[f'{self.thumb_path}'] = open(self.thumb_path, 'rb')
        
        return data, media

class InputMediaPhoto(InputMedia):
    def __init__(self, media_path, caption=""):
        super().__init__("photo", media_path, "", caption)

class InputMediaVideo(InputMedia):
    def __init__(self, media_path, thumb_path="", caption="", width=0, height=0, duration=0, supports_streaming=True):
        super().__init__("video", media_path, thumb_path, caption)
        self.width = width
        self.height = height
        self.duration = duration
        self.supports_streaming = supports_streaming
    
    def toDict(self):
        data, media = super().toDict()
        data['width'] = self.width if self.width > 0 else None
        data['height'] = self.height if self.height > 0 else None
        data['duration'] = self.duration if self.duration > 0 else None
        data['supports_streaming'] = self.supports_streaming if self.supports_streaming else False

        return data, media

class InputMediaAnimation(InputMedia):
    def __init__(self, media_path, thumb_path="", caption="", width=0, height=0, duration=0):
        super().__init__("animation", media_path, thumb_path, caption)
        self.width = width
        self.height = height
        self.duration = duration
    
    def toDict(self):
        data, media = super().toDict()
        data['width'] = self.width if self.width > 0 else None
        data['height'] = self.height if self.height > 0 else None
        data['duration'] = self.duration if self.duration > 0 else None

        return data, media

class InputMediaAudio(InputMedia):
    def __init__(self, media_path, thumb_path="", caption="", duration=0, performer="", title=""):
        super().__init__("audio", media_path, thumb_path, caption)
        self.duration = duration
        self.performer = performer
        self.title = title
    
    def toDict(self):
        data, media = super().toDict()
        data['duration'] = self.duration if self.duration > 0 else None
        data['performer'] = self.performer if self.performer else None
        data['title'] = self.title if self.title else None

        return data, media

class InputMediaDocument(InputMedia):
    def __init__(self, media_path, thumb_path="", caption=""):
        super().__init__("document", media_path, thumb_path, caption)

class InputMediaList:
    def __init__(self):
        self.__list = []

    def append(self, input_media):
        if isinstance(input_media, InputMedia):
            self.__list.append(input_media)
            return self
        
        raise ValueError("Passed parameter is not type or does not inherit from type InputMedia")
    
    def toDict(self):
        result_data = []
        result_media = {}
        for media in self.__list:
            media_data, media_media = media.toDict()
            result_data.append(media_data)
            result_media = result_media | media_media

        return result_data, result_media

