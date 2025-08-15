"""User Class and UserManager Class"""

from src.globals import *
from src.help_functions import *
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
        sql_text = "SELECT id, login, name, surname FROM users WHERE deleted = false;"
        result = query_select(
            sql_text, dict_result=True)
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
        sql_text = "SELECT id FROM users WHERE login = :login AND deleted = false;"
        result = query_select_one(sql_text, {"login": login})
        if result:
            return result[0] > 0
        else:
            return False

    def get_user_by_login(self, login):
        if not login:
            print("Login cannot be empty.")
            return

        result_user = User()
        sql_text = "SELECT id, login, name, surname FROM users WHERE login = :login AND deleted = false;"
        result = query_select_one(sql_text, {"login": login}, dict_result=True)
        if result:
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

        sql_text = "SELECT password FROM users WHERE login = :login AND deleted = false;"
        result = query_select_one(sql_text, {"login": login})
        if not result or not check_hashed(password, result[0]):
            print("Incorrect password.")
            return False
        else:
            self.logged_user = self.get_user_by_login(login)
            if self.is_logged:
                print("Logged in successfully!")

            return True

    def log_out(self):
        self.logged_user.set_defaults()

    def add_user(self, login, name, surname, password):
        sql_text = "INSERT INTO users (name, surname, login, password) VALUES (:name_in, :surname_in, :login_in, :password_in)"
        user_in = {
            "name_in": name,
            "surname_in": surname,
            "login_in": login,
            "password_in": hash_text(password)
        }
        result = query_insert(sql_text, user_in)

        return result

    def delete_user(self, login):
        sql_text = "UPDATE users SET deleted = true WHERE login = :login_in;"
        result = query_update(sql_text, {"login_in": login})
        return result

    def register_ip(self, ip_address):
        if not self.is_logged:
            print("User is not logged in.")
            return

        print(f"Current IP: {ip_address}")
        if ip_address:
            print("Registering IP address...")
            sql_text = "UPDATE users SET ip_address = :ip_address WHERE id = :user_id;"
            params = {"user_id": self.logged_user.id, "ip_address": ip_address}
            query_update(sql_text, params)
            return
        else:
            print("Could not retrieve current IP.")


# Global instance
user_manager = UserManager()
