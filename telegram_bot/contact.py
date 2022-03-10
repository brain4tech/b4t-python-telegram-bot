# class for contact

class Contact:
    def __init__(self, data_: dict):
        self.phone_number = data_['phone_number']
        self.first_name = data_['first_name']
        self.last_name = data_['last_name'] if 'last_name' in data_ else None
        self.user_id = data_['user_id'] if 'user_id' in data_ else None
        self.vcard = data_['vcard'] if 'vcard' in data_ else None