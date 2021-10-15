
class ChatPermissions:
    def __init__(self, send_messages = False, send_media_messages = False, send_polls = False, send_other_messages = False, add_web_page_previews = False, change_info = False, invite_users = False, pin_messages = False):
        self.can_send_messages = send_messages
        self.can_send_media_messages = send_media_messages
        self.can_send_polls = send_polls
        self.can_send_other_messages = send_other_messages
        self.can_add_page_previews = add_web_page_previews
        self.can_change_info = change_info
        self.can_invite_users = invite_users
        self.can_pin_messages = pin_messages
    
    def toDict (self):
        return self.__dict__

if __name__ == '__main__':
    test = ChatPermissions(True, False, True, False, True, True, False, False)
    print (test.toDict())
