"""User management module"""

import psycopg2
import sqlite3

from src.globals import *
from src.help_functions import hash_text, check_hashed
from src.class_db import connection_manager
from src.db_functions import *


user_defaults = {
    "id": "",
    "login": "",
    "name": "",
    "surname": ""
}


class UserManager:
    def __init__(self):  # constructor
        self.logged_user = user_defaults

    @property
    def is_logged(self):
        return (self.logged_user["login"] != "")

    @property
    def is_super_admin(self):
        return (self.logged_user["login"] == "SuperAdmin")

    def get_login_list(self):  # lista użytkowników
        try:
            table = "users"
            fields = ["login"]
            where_clause = "deleted = false"
            select_result = query_select(table, fields, where_clause)
            return [row[0] for row in select_result]
        except Exception as e:
            print(e)
            return []

    # czy istnieje użytkownik (nieusunięty) o tym loginie
    def check_if_user_exists(self, login):
        if connection_manager.connection:
            cursor = connection_manager.db_cursor
            cursor.execute(
                "SELECT id FROM users WHERE login = %s AND deleted = false;", (login,))
            return bool(cursor.fetchone())
        else:
            print("No connection...")
            return False

    def get_user_by_login(self, login):  # pobranie danych użytkownika po loginie
        cursor = connection_manager.db_cursor_dict
        cursor.execute(
            "SELECT id, name, surname FROM users WHERE login = %s AND deleted = false;", (login,))
        return cursor.fetchone()

    def log_in(self, login, password) -> bool:  # logowanie użytkownika
        # superadmin (bez połączenia z bazą)
        if login == "SuperAdmin":
            if password == "0000":
                print("Zalogowano pomyślnie!")
                self.logged_user["id"] = "-1"
                self.logged_user["login"] = login
                self.logged_user["name"] = ""
                self.logged_user["surname"] = ""
                return True
            else:
                print("Nieprawidłowe hasło.")
                return False

        # logowanie z bazy
        cursor = connection_manager.db_cursor
        cursor.execute(
            "SELECT * FROM users WHERE login = %s AND deleted = false;", (login,))
        result = cursor.fetchone()
        if not result:
            print("Nie ma takiego użytkownika.")
        elif not check_hashed(password, result['password']):
            print("Nieprawidłowe hasło.")
        else:
            print("Zalogowano pomyślnie!")
            self.logged_user["id"] = result["id"]
            self.logged_user["login"] = result["login"]
            self.logged_user["name"] = result["name"]
            self.logged_user["surname"] = result["surname"]
            return True
        return False

    def log_out(self):
        self.logged_user = {"id": "", "login": "", "name": "", "surname": ""}

    def add_user(self, login, name, surname, password):
        cursor = connection_manager.db_cursor
        cursor.execute("INSERT INTO users (name, surname, login, password) VALUES (%s, %s, %s, %s);",
                       (name, surname, login, hash_text(password)))
        connection_manager.connection.commit()
        return cursor.rowcount

    def delete_user(self, login):
        cursor = connection_manager.db_cursor
        cursor.execute(
            "UPDATE users SET deleted = true WHERE login = %s;", (login,))
        connection_manager.connection.commit()
        return cursor.rowcount


# Global instance
user_manager = UserManager()
