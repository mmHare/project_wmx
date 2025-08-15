"""User class used as program account"""


class User:
    def __init__(self):
        self.set_defaults()

    def set_defaults(self):
        self.id = ""
        self.login = ""
        self.name = ""
        self.surname = ""
        self.ip_address = ""
