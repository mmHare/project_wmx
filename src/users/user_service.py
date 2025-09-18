"""Service class for users management"""

from src.globals.help_functions import get_local_ip
from src.users.class_user import User
from .user_manager import get_user_manager


class classproperty(property):
    def __get__(self, instance, owner):
        return self.fget(owner)


class UserService:
    _user_manager = get_user_manager()

    @classproperty
    def is_logged(cls) -> bool:
        return cls._user_manager.is_logged

    @classproperty
    def logged_user(cls) -> User:
        return cls._user_manager.logged_user

    @classmethod
    def get_logged_user_info(cls) -> str:
        if cls._user_manager.is_logged:
            return str(cls._user_manager.logged_user)
        return "No user is logged in."

    @classmethod
    def get_user_guid(cls, user_id: int | str):
        return cls._user_manager.get_user_guid(user_id)

    @classmethod
    def log_out(cls):
        cls._user_manager.log_out()
        return cls._user_manager.is_logged

    @classmethod
    def register_user(cls):
        local_ip = get_local_ip()
        print(f"Register current IP ({local_ip})? (y/n)")
        if input().strip().lower() == "y":
            cls._user_manager.register_ip(local_ip)
