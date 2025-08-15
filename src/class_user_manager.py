"""User management module"""

import psycopg2
import sqlite3

from src.globals import *
from src.help_functions import hash_text, check_hashed
from src.class_db import connection_manager
from src.db_functions import *


class User:
    def __init__(self):
        self.set_defaults()

    def set_defaults(self):
        self.id = ""
        self.login = ""
        self.name = ""
        self.surname = ""


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

    def get_login_list(self):  # lista użytkowników
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

        # result_user = dict()
        # result = query_select_one(
        #     "SELECT id, name, surname FROM users WHERE login = %s AND deleted = false;", {"login": login})
        # if result is None:
        #     result_user["id"] = result[0]
        #     result_user["login"] = result[1]
        #     result_user["name"] = result[2]
        #     result_user["surname"] = result[3]

        # try:
        #     table = "users"
        #     fields = ["login"]
        #     where_clause = "deleted = false"
        #     select_result = query_select(table, fields, where_clause)
        #     return [row[0] for row in select_result]
        # except Exception as e:
        #     print(e)
        #     return []

    # czy istnieje użytkownik (nieusunięty) o tym loginie
    def check_if_user_exists(self, login):
        result = query_select_one(
            "SELECT id FROM users WHERE login = :login AND deleted = false;", {"login": login})
        if result is not None:
            return result[0] > 0
        else:
            return False

        # if connection_manager.connection:
        #     cursor = connection_manager.db_cursor
        #     cursor.execute(
        #         "SELECT id FROM users WHERE login = %s AND deleted = false;", (login,))
        #     return bool(cursor.fetchone())
        # else:
        #     print("No connection...")
        #     return False

    def get_user_by_login(self, login):  # pobranie danych użytkownika po loginie
        if not login:
            print("Login cannot be empty.")
            return

        result_user = User()
        result = query_select_one(
            "SELECT id, name, surname FROM users WHERE login = %s AND deleted = false;", {"login": login})
        if result is None:
            result_user.id = result[0]
            result_user.login = result[1]
            result_user.name = result[2]
            result_user.surname = result[3]

        return result_user

        # cursor = connection_manager.db_cursor_dict
        # cursor.execute(
        #     "SELECT id, name, surname FROM users WHERE login = %s AND deleted = false;", (login,))
        # return cursor.fetchone()

    def log_in(self, login, password) -> bool:  # logowanie użytkownika
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
            # self.logged_user["id"] = result["id"]
            # self.logged_user["login"] = result["login"]
            # self.logged_user["name"] = result["name"]
            # self.logged_user["surname"] = result["surname"]
            return True
        # return False

        # # superadmin (bez połączenia z bazą)
        # if login == "SuperAdmin":
        #     if password == "0000":
        #         print("Zalogowano pomyślnie!")
        #         self.logged_user["id"] = "-1"
        #         self.logged_user["login"] = login
        #         self.logged_user["name"] = ""
        #         self.logged_user["surname"] = ""
        #         return True
        #     else:
        #         print("Nieprawidłowe hasło.")
        #         return False

        # # logowanie z bazy
        # cursor = connection_manager.db_cursor
        # cursor.execute(
        #     "SELECT * FROM users WHERE login = %s AND deleted = false;", (login,))
        # result = cursor.fetchone()
        # if not result:
        #     print("Nie ma takiego użytkownika.")
        # elif not check_hashed(password, result['password']):
        #     print("Nieprawidłowe hasło.")
        # else:
        #     print("Zalogowano pomyślnie!")
        #     self.logged_user["id"] = result["id"]
        #     self.logged_user["login"] = result["login"]
        #     self.logged_user["name"] = result["name"]
        #     self.logged_user["surname"] = result["surname"]
        #     return True
        # return False

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

        # cursor = connection_manager.db_cursor
        # cursor.execute("INSERT INTO users (name, surname, login, password) VALUES (%s, %s, %s, %s);",
        #                (name, surname, login, hash_text(password)))
        # connection_manager.connection.commit()
        # return cursor.rowcount

    def delete_user(self, login):
        result = query_update(
            "UPDATE users SET deleted = true WHERE login = :login_in;", {"login_in": login})
        return result

        # cursor = connection_manager.db_cursor
        # cursor.execute(
        #     "UPDATE users SET deleted = true WHERE login = %s;", (login,))
        # connection_manager.connection.commit()
        # return cursor.rowcount


# Global instance
user_manager = UserManager()
