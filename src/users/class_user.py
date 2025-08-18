"""User class used as program account"""


from src.globals import UserRole


class User:
    def __init__(self):
        self.set_defaults()

    def set_defaults(self):
        self.id = 0
        self.login = ""
        self.name = ""
        self.surname = ""
        self.ip_address = ""
        self.user_role = UserRole.USER

    @property
    def is_admin(self):
        return self.user_role == UserRole.ADMIN
