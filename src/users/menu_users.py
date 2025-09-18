"""Class with menu options"""

import getpass
from src.class_menu import MenuOption, MenuScreen
from src.database.database_service import DatabaseService
from src.globals.glob_enums import UserRole
from src.globals.help_functions import get_local_ip
from .class_user import User
from .user_manager import get_user_manager
from .user_service import UserService
from .users_conversation import Conversation


class UsersMenu(MenuScreen):
    _user_manager = get_user_manager()

    def __init__(self):
        super().__init__("User settings")

    def prepare_list(self):
        result_list = []
        if DatabaseService.is_connected and not self._user_manager.is_logged:
            result_list.append(MenuOption(
                "Log in", UsersMenu.user_log_in))

        result_list.append(MenuOption(
            "User list", UsersMenu.list_users))
        result_list.append(MenuOption(
            "Add new user", self.new_user))

        if DatabaseService.is_connected and self._user_manager.is_logged:
            if UserService.logged_user.is_admin:
                result_list.append(MenuOption(
                    "Delete user", self.delete_user))
            result_list.append(MenuOption(
                "Conversation", self.user_conversation))
            result_list.append(MenuOption.from_func(
                self.__register_user_func))
            result_list.append(MenuOption(
                "Log out", UsersMenu.user_log_out))

        self.info_top = UserService.get_logged_user_info()
        return result_list

    def __register_user_func(self) -> tuple:
        if self._user_manager.is_logged:
            local_ip = get_local_ip()
            return f"Register IP ({local_ip})", UserService.register_user
        else:
            return None, None

    @classmethod
    def user_log_in(cls):
        return cls._user_manager.log_in(input("Login: "), getpass.getpass("Password: "))

    @classmethod
    def user_log_out(cls):
        result = input("Do you really want to log out? (y/n): ")
        if result.strip().lower() == "y":
            return UserService.log_out()
        return False

    @classmethod
    def list_users(cls):
        print("Users:")
        for user in cls._user_manager.get_login_list():
            print(
                f"  {user.login} ({user.ip_address if user.ip_address else 'No IP registered'})")

    def new_user(self):
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
                if not self._user_manager.check_if_user_exists(login):
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
            self._user_manager.add_user(user, password)

    def delete_user(self):
        print("Delete user")
        while True:
            login = input("Login: ")
            if login == "":
                return
            if login == UserService.logged_user.login:
                print("You cannot delete yourself.")
                continue
            if self._user_manager.check_if_user_exists(login):
                choice = input(f"Do you want to delete user {login}? (y/n): ")
                if choice.strip().lower() == "y":
                    self._user_manager.delete_user(login)
                    print(f"User {login} deleted.")
                else:
                    print(f"User {login} not deleted.")
            else:
                print(f"User {login} does not exist.")

    @classmethod
    def user_conversation(cls):
        login = input("Enter login of user to start conversation:")

        if login == "":
            return
        if login == UserService.logged_user.login:
            print("You cannot choose yourself.")
            return

        if not cls._user_manager.check_if_user_exists(login):
            print(f"User {login} is not available")
            return

        peer_guid = cls._user_manager.get_user_guid(login)
        conversation = Conversation(UserService.logged_user, peer_guid)
        conversation.start()
