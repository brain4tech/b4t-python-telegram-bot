# classes for media

class PhotoSize:
    def __init__(self, data_: dict):
        self.file_id = data_['file_id']
        self.file_unique_id = data_['file_unique_id']
        self.width = data_['width']
        self.height = data_['height']
        self.size = data_['size'] if 'size' in data_ else None

class Video:
    def __init__(self, data_: dict):
        self.file_id = data_['file_id']
        self.file_unique_id = data_['file_unique_id']
        self.width = data_['width']
        self.height = data_['height']
        self.duration = data_['duration']
        self.thumb = PhotoSize(data_['thumb']) if 'thumb' in data_ else None
        self.file_name = data_['file_name'] if 'file_name' in data_ else None
        self.file_size = data_['file_size'] if 'file_size' in data_ else None

class Animation(Video):
    def __init__(self, data_: dict):
        super().__init__(data_)

class Audio:
    def __init__(self, data_: dict):
        self.file_id = data_['file_id']
        self.file_unique_id = data_['file_unique_id']
        self.duration = data_['duration']
        self.performer = data_['performer'] if 'performer' in data_ else None
        self.title = data_['title'] if 'title' in data_ else None
        self.file_name = data_['file_name'] if 'file_name' in data_ else None
        self.file_size = data_['file_size'] if 'file_size' in data_ else None
        self.thumb = PhotoSize(data_['thumb']) if 'thumb' in data_ else None

class Document:
    def __init__(self, data_: dict):
        self.file_id = data_['file_id']
        self.file_unique_id = data_['file_unique_id']
        self.thumb = PhotoSize(data_['thumb']) if 'thumb' in data_ else None
        self.file_name = data_['file_name'] if 'file_name' in data_ else None
        self.file_size = data_['file_size'] if 'file_size' in data_ else None
