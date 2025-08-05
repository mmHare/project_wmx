'''User management module'''

import getpass
from src.mod_db import connection_manager
from src.func_utils import hash_text, check_hashed


# klasa managera użytkowników
class UserManager:
    logged_user = {"id": "", "login": "", "name": "", "surname": ""}

    def __init__(self):  # constructor
        pass

    @property
    def is_logged(self):
        return (self.logged_user["login"] != "")

    @property
    def is_super_admin(self):
        return (self.logged_user["login"] == "SuperAdmin")

    def get_login_list(self):  # lista użytkowników
        cursor = connection_manager.db_cursor
        cursor.execute("SELECT login from users where deleted = false;")
        return [row["login"] for row in cursor.fetchall()]

    # czy istnieje użytkownik (nieusunięty) o tym loginie
    def check_if_user_exists(self, login):
        cursor = connection_manager.db_cursor
        cursor.execute(
            "SELECT id FROM users WHERE login = %s AND deleted = false;", (login,))
        return bool(cursor.fetchone())

    def get_user_by_login(self, login):  # pobranie danych użytkownika po loginie
        cursor = connection_manager.db_cursor
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

    # ekran ustawień użytkowników

    def user_management_screen(self):
        while True:
            print("\n"*3)
            print("---Użytkownicy---")
            print("Zalogowany użytkownik: {}".format(
                self.logged_user["login"]))
            print("1. Wyloguj" if self.is_logged else "1. Zaloguj")
            print("2. Lista użytkowników")
            print("3. Dodaj użytkownika")
            print("4. Usuń użytkownika")
            print("0. Wyjście")
            user_input = input()

            # wyjście
            if user_input.lower() in ["0", "q", "quit"]:
                return
            # logowanie/wylogowanie
            elif user_input == "1":
                if self.is_logged:
                    self.log_out()
                else:
                    self.log_in(input("Login: "), getpass.getpass("Hasło: "))
            # lista userów
            elif user_input == "2":
                print("Użytkownicy:")
                usr_list = self.get_login_list()
                for item in usr_list:
                    print(item)
                input("Naciśnij ENTER")
            # dodawanie usera
            elif user_input == "3":
                print("Nowy użytkownik")
                login = input("Login: ")
                name = input("Imię: ")
                surname = input("Surname: ")
                password = getpass.getpass("Hasło: ")
                self.add_user(login, name, surname, password)
            # usuwanie usera
            elif user_input == "4":
                print("Usuwanie użytkownika")
                self.delete_user(input("Login: "))

    def user_settings(self):
        self.user_management_screen()


user_manager = UserManager()  # instancja klasy UserManager
