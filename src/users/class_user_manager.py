"""User Class and UserManager Class"""

from src.globals import *
from src.help_functions import hash_text, check_hashed
from src.database import *
from .class_user import User


class UserManager:
    def __init__(self):  # constructor
        self.logged_user = User()
        self.logged_user.set_defaults()

    @property
    def is_logged(self):
        return (self.logged_user.login != "")

    @property
    def is_super_admin(self):
        return (self.logged_user.login == "SuperAdmin")

    def get_login_list(self):
        result_list = []
        result = query_select(
            "SELECT id, login, name, surname FROM users WHERE deleted = false;", dict_result=True)
        if result:
            for item in result:
                user = User()
                user.id = item.get("id", "")
                user.login = item.get("login", "")
                user.name = item.get("name", "")
                user.surname = item.get("surname", "")
                result_list.append(user)
        return result_list

    # if there is a user with the given login (not deleted)
    def check_if_user_exists(self, login):
        result = query_select_one(
            "SELECT id FROM users WHERE login = :login AND deleted = false;", {"login": login})
        if result is not None:
            return result[0] > 0
        else:
            return False

    def get_user_by_login(self, login):
        if not login:
            print("Login cannot be empty.")
            return

        result_user = User()
        result = query_select_one(
            "SELECT id, name, surname FROM users WHERE login = %s AND deleted = false;", {"login": login}, dict_result=True)
        if result is None:
            result_user.id = result.get("id", "")
            result_user.login = result.get("login", "")
            result_user.name = result.get("name", "")
            result_user.surname = result.get("surname", "")

        return result_user

    def log_in(self, login, password) -> bool:
        if not self.check_if_user_exists(login):
            print("Incorrect login.")
            return False
        if not password:
            print("Password cannot be empty.")
            return False

        result = query_select_one(
            "SELECT password FROM users WHERE login = %s AND deleted = false;", {"login": login})
        if not check_hashed(password, result[0]):
            print("Incorrect password.")
            return False
        else:
            self.logged_user = self.get_user_by_login(login)
            print("Logged in successfully!")

            return True

    def log_out(self):
        self.logged_user.set_defaults()

    def add_user(self, login, name, surname, password):
        user_in = {
            "name_in": name,
            "surname_in": surname,
            "login_in": login,
            "password_in": hash_text(password)
        }
        result = query_insert(
            "INSERT INTO users (name, surname, login, password) VALUES (:name_in, :surname_in, :login_in, :password_in)", user_in)

        return result

    def delete_user(self, login):
        result = query_update(
            "UPDATE users SET deleted = true WHERE login = :login_in;", {"login_in": login})
        return result


# Global instance
user_manager = UserManager()
