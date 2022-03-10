# class for location and venue

class Location:
    def __init__(self, data_: dict):
        self.longitude = data_['longitude']
        self.latitude = data_['latitude']
        self.horizontal_accuracy = data_['horizontal_accuracy'] if 'horizontal_accuracy' in data_ else None


class Venue:
    def __init__ (self, data_: dict):
        self.location = Location(data_['location'])
        self.title = data_['title']
        self.address = data_['address']
