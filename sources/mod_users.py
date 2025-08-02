'''User management module'''

import psycopg2
from psycopg2.extras import RealDictCursor
import getpass

# połączenie z bazą


def create_connection():
    try:
        connection = psycopg2.connect(
            database="project_db",
            user="db_user",
            password="user",
            host="192.168.0.11",
            port=5432
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None


def close_connection(conn):
    if conn:
        conn.close()


# klasa managera użytkowników
class User_manager:
    logged_user = {"id": "", "login": "", "name": "", "surname": ""}

    def __init__(self):  # constructor
        self.connection = create_connection()

    @property
    def db_cursor(self):
        # RealDictCursor żeby był dostęp wartości po nazwach
        return self.connection.cursor(cursor_factory=RealDictCursor)

    @property
    def is_logged(self):
        return (self.logged_user["login"] != "")

    @property
    def is_super_admin(self):
        return (self.logged_user["login"] == "SuperAdmin")

    def get_login_list(self):  # lista użytkowników
        cursor = self.db_cursor
        cursor.execute("SELECT login from users where deleted = false;")
        return [row["login"] for row in cursor.fetchall()]

    # czy istnieje użytkownik (nieusunięty) o tym loginie
    def check_if_user_exists(self, login):
        cursor = self.db_cursor
        cursor.execute(
            "SELECT id FROM users WHERE login = %s AND deleted = false;", (login,))
        return bool(cursor.fetchone())

    def get_user_by_login(self, login):  # pobranie danych użytkownika po loginie
        cursor = self.db_cursor
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
        cursor = self.db_cursor
        cursor.execute(
            "SELECT * FROM users WHERE login = %s AND deleted = false;", (login,))
        result = cursor.fetchone()
        if not result:
            print("Nie ma takiego użytkownika.")
        elif result['password'] != password:
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
        cursor = self.db_cursor
        cursor.execute("INSERT INTO users (name, surname, login, password) VALUES (%s, %s, %s, %s);",
                       (name, surname, login, password))
        self.connection.commit()
        return cursor.rowcount

    def delete_user(self, login):
        cursor = self.db_cursor
        cursor.execute(
            "UPDATE users SET deleted = true WHERE login = %s;", (login,))
        self.connection.commit()
        return cursor.rowcount


# ekran ustawień użytkowników
def user_management_screen(usr_man: User_manager):
    while True:
        print("\n"*3)
        print("---Użytkownicy---")
        print("Zalogowany użytkownik: {}".format(
            usr_man.logged_user["login"]))
        print("1. Wyloguj" if usr_man.is_logged else "1. Zaloguj")
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
            if usr_man.is_logged:
                usr_man.log_out()
            else:
                usr_man.log_in(input("Login: "), getpass.getpass("Hasło: "))
        # lista userów
        elif user_input == "2":
            print("Użytkownicy:")
            usr_list = usr_man.get_login_list()
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
            usr_man.add_user(login, name, surname, password)
        # usuwanie usera
        elif user_input == "4":
            print("Usuwanie użytkownika")
            usr_man.delete_user(input("Login: "))
