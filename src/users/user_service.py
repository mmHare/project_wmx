"""Functions for users management"""

import getpass

from src.globals import UserRole
from src.globals.help_functions import get_local_ip
from .class_user import User
from .class_user_manager import get_user_manager
from .users_conversation import Conversation
# from . import User, Conversation, get_user_manager


class UserService:
    _user_manager = get_user_manager()

    @classmethod
    def menu_register_user(cls) -> tuple:
        if cls._user_manager.is_logged:
            local_ip = get_local_ip()
            return f"Register IP ({local_ip})", cls.register_user
        else:
            return None, None

    @classmethod
    def get_logged_user_info(cls):
        if cls._user_manager.is_logged:
            user = cls._user_manager.logged_user
            return f"{user.user_role.name.capitalize()}: {user.login} - {user.name} {user.surname}"
        return "No user is logged in."

    @classmethod
    def get_user_guid(cls, user_id: int | str):
        return cls._user_manager.get_user_guid(user_id)

    @classmethod
    def log_out_silent(cls):
        cls._user_manager.log_out()
        return cls._user_manager.is_logged


# Menu options
# user_manager = get_user_manager()

    @classmethod
    def menu_user_log_in(cls):
        return cls._user_manager.log_in(input("Login: "), getpass.getpass("Password: "))

    @classmethod
    def menu_user_log_out(cls):
        result = input("Do you really want to log out? (y/n): ")
        if result.strip().lower() == "y":
            return cls._user_manager.log_out()
        return False

    @classmethod
    def menu_list_users(cls):
        print("Users:")
        for user in cls._user_manager.get_login_list():
            print(
                f"  {user.login} ({user.ip_address if user.ip_address else 'No IP registered'})")

    @classmethod
    def menu_new_user(cls):
        def validate_text(text: str):
            if len(text) < 3:
                print("Must be at least 3 characters long.")
                return False
            elif any(c.isspace() for c in text):
                print("Cannot include whitespaces.")
                return False
            elif not text.isalnum():
                print("Login must be alphanumeric.")
                return False
            return True

        print("New user")
        user = User()
        failed_count = 0
        while True:
            login = input("Login: ")
            if login == "q":
                print("Cancelling operation...")
                return
            if validate_text(login):
                if not cls._user_manager.check_if_user_exists(login):
                    user.login = login
                    break
                else:
                    print("User already exists.")
            else:
                failed_count += 1
                if failed_count > 2:
                    print("Cancelling operation...")
                    return

        user.name = input("Name: ")
        user.surname = input("Surname: ")
        while True:
            password = getpass.getpass("Password: ")
            if validate_text(password):
                break

        while True:
            user_role = input("User role (admin/user): ")
            if user_role in ["admin", "user"]:
                user.user_role = UserRole.ADMIN if user_role == "admin" else UserRole.USER
                break
            print("Invalid role. Please enter 'admin' or 'user'.")

        choice = input(f"Do you want to create user {login}? (y/n): ")
        if choice.strip().lower() == "y":
            cls._user_manager.add_user(user, password)

    @classmethod
    def menu_delete_user(cls):
        print("Delete user")
        while True:
            login = input("Login: ")
            if login == "":
                return
            if login == cls._user_manager.logged_user.login:
                print("You cannot delete yourself.")
                continue
            if cls._user_manager.check_if_user_exists(login):
                choice = input(f"Do you want to delete user {login}? (y/n): ")
                if choice.strip().lower() == "y":
                    cls._user_manager.delete_user(login)
                    print(f"User {login} deleted.")
                else:
                    print(f"User {login} not deleted.")
            else:
                print(f"User {login} does not exist.")

    @classmethod
    def menu_user_conversation(cls):
        login = input("Enter login of user to start conversation:")

        if login == "":
            return
        if login == cls._user_manager.logged_user.login:
            print("You cannot choose yourself.")
            return

        if not cls._user_manager.check_if_user_exists(login):
            print(f"User {login} is not available")
            return

        peer_guid = cls._user_manager.get_user_guid(login)
        conversation = Conversation(cls._user_manager.logged_user, peer_guid)
        conversation.start()

    @classmethod
    def register_user(cls):
        local_ip = get_local_ip()
        print(f"Register current IP ({local_ip})? (y/n)")
        if input().strip().lower() == "y":
            cls._user_manager.register_ip(local_ip)
