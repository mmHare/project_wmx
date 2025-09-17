"""User Class and UserManager Class"""

import datetime
import uuid
from src.database.database_service import DatabaseService
from src.globals.glob_enums import UserRole
from src.globals.help_functions import check_hashed, hash_text
from .class_user import User


class UserManager:
    def __init__(self):  # constructor
        self.logged_user = User()
        self.logged_user.set_defaults()

    @property
    def is_logged(self):
        return (self.logged_user.login != "")

    @property
    def logged_user_guid(self):
        if self.logged_user.id > 0:
            return self.get_user_guid(self.logged_user.id)
        else:
            ""

    def get_login_list(self) -> list[User]:
        result_list = []
        sql_text = "SELECT * FROM users WHERE deleted_at is NULL;"
        result = DatabaseService.query_select(
            sql_text, dict_result=True)
        if result:
            for item in result:
                user = User()
                user.id = item.get("id", "")
                user.login = item.get("login", "")
                user.name = item.get("name", "")
                user.surname = item.get("surname", "")
                user.ip_address = item.get("ip_address", "")
                try:
                    user.user_role = UserRole(item.get("user_role", 0))
                except ValueError:
                    user.user_role = UserRole.NONE
                result_list.append(user)
        return result_list

    # if there is a user with the given login (not deleted)
    def check_if_user_exists(self, login):
        sql_text = "SELECT id FROM users WHERE login = :login AND deleted_at is NULL;"
        params = {"login": login}
        result = DatabaseService.query_select_one(sql_text, params)
        if result:
            return result[0] > 0
        else:
            return False

    def get_user_by_login(self, login):
        if not login:
            print("Login cannot be empty.")
            return

        user = User()
        db_kind = DatabaseService.get_db_kind_connection()
        sql_text = "SELECT * FROM users WHERE login = :login AND deleted_at is NULL;"
        result = DatabaseService.query_select_one(
            sql_text, {"login": login}, dict_result=True)
        if result:
            user.id = result.get("id", "")
            user.login = result.get("login", "")
            user.name = result.get("name", "")
            user.surname = result.get("surname", "")
            user.ip_address = result.get("ip_address", "")
            user.db_kind = db_kind
            try:
                user.user_role = UserRole(result.get("user_role", 0))
            except ValueError:
                user.user_role = UserRole.NONE
        return user

    def log_in(self, login, password) -> bool:
        if not self.check_if_user_exists(login):
            print("Incorrect login.")
            return False
        if not password:
            print("Password cannot be empty.")
            return False

        sql_text = "SELECT password FROM users WHERE login = :login AND deleted_at is NULL;"
        result = DatabaseService.query_select_one(sql_text, {"login": login})
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

    def add_user(self, user: User, password):
        sql_text = "INSERT INTO users (name, surname, login, password, user_role, guid) VALUES (:name_in, :surname_in, :login_in, :password_in, :user_role_in, :guid)"
        user_in = {
            "name_in": user.name,
            "surname_in": user.surname,
            "login_in": user.login,
            "password_in": hash_text(password),
            "user_role_in": user.user_role.value,
            "guid": str(uuid.uuid4())
        }
        result = DatabaseService.query_insert(sql_text, user_in)
        return result

    def get_user_guid(self, user_id: int | str):
        try:
            if isinstance(user_id, int):
                sql_text = "SELECT guid FROM users WHERE id = :id;"
                result = DatabaseService.query_select_one(
                    sql_text, {"id": user_id})
            elif isinstance(user_id, str):
                sql_text = "SELECT guid FROM users WHERE login = :login;"
                result = DatabaseService.query_select_one(
                    sql_text, {"login": user_id})
            else:
                raise ValueError("Type not supported.")
            return uuid.UUID(result[0])
        except:
            return None

    def delete_user(self, login):
        sql_text = "UPDATE users SET deleted_at = :deleted_at WHERE login = :login_in;"
        params = {"deleted_at": datetime.now(
            datetime.timezone.utc), "login_in": login}
        result = DatabaseService.query_update(sql_text, params)
        return result

    def register_ip(self, ip_address):
        if not self.is_logged:
            print("User is not logged in.")
            return

        print("Registering IP address...")
        if ip_address:
            sql_text = "UPDATE users SET ip_address = :ip_address WHERE id = :user_id;"
            params = {"user_id": self.logged_user.id, "ip_address": ip_address}
            DatabaseService.query_update(sql_text, params)
            print("Successfully registered IP address.")
            return
        else:
            print("Could not retrieve current IP.")


# Instance
_user_manager = None


def get_user_manager():
    global _user_manager
    if _user_manager is None:
        _user_manager = UserManager()
    return _user_manager
