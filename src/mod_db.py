'''Database connection module for the project.'''

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3

from src.constants import *
from src.enums_and_dicts import DB_VERSION, DbType


class ConnectionManager:
    """Class to manage database connections and operations."""

    def __init__(self, db_type: DbType = DbType.POSTGRES):
        self.db_type = db_type
        self.connection = None
        self.connection = self.connect()
        if not self.connection:
            raise Exception("Failed to connect to the database.")

    @property
    def db_cursor(self):
        """Database cursor property."""
        if self.connection is None:
            raise Exception("Database connection is not established.")
        else:
            return self.connection.cursor()

    def db_cursor_dict(self):
        """Returns a cursor with dictionary-like access."""
        if self.connection is None:
            raise Exception("Database connection is not established.")
        if self.db_type == DbType.POSTGRES:
            return self.connection.cursor(cursor_factory=RealDictCursor)
        else:
            raise Exception(
                "Dictionary cursor is only available for PostgreSQL.")

    def __del__(self):
        self.close_connection()

    def connect(self):
        self.close_connection()
        try:
            if self.db_type == DbType.POSTGRES:
                connection = psycopg2.connect(
                    database="project_db",
                    user="db_user",
                    password="user",
                    host="192.168.0.11",
                    port=5432
                )
                return connection
            elif self.db_type == DbType.SQLITE:
                if not os.path.exists(DB_FILE_DIR + "/project_db.sqlite"):
                    if input("Database file not found. Do you want to create it? (y/n): ").lower() != 'y':
                        return None
                if not os.path.exists(DB_FILE_DIR):
                    os.makedirs(DB_FILE_DIR, exist_ok=True)
                connection = sqlite3.connect(
                    DB_FILE_DIR + "/project_db.sqlite")
                return connection
            else:
                return None
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def update_db(self):
        """Method to update the database schema."""
        if self.connection:
            cursor = self.db_cursor
            file = open(
                f"src/sql/{self.db_type.value}/schema/create_tables.sql", 'r')
            sql = " ".join(file.readlines())
            if self.db_type == DbType.POSTGRES:
                cursor.execute(sql)
            elif self.db_type == DbType.SQLITE:
                for statement in sql.split(';'):
                    if statement.strip():
                        cursor.execute(statement)
            self.connection.commit()
            self.set_db_version(DB_VERSION[self.db_type])
            print("Database updated successfully.")
            return True
        else:
            return False

    def set_db_version(self, version: str):
        """Method to set the database version."""
        if self.connection:
            cursor = self.db_cursor
            if self.db_type == DbType.POSTGRES:
                cursor.execute(
                    "INSERT INTO configuration (key_name, value_str) VALUES (%s, %s) ON CONFLICT (key_name) DO UPDATE SET value_str = %s;",
                    ("db_version", version, version))
            elif self.db_type == DbType.SQLITE:
                cursor.execute(
                    "INSERT OR REPLACE INTO configuration (key_name, value_str) VALUES (?, ?);",
                    ("db_version", version))
            self.connection.commit()

    def check_db_version(self):
        if self.connection:
            cursor = self.db_cursor
            try:
                if self.db_type == DbType.POSTGRES:
                    sql_text = "SELECT value_str FROM configuration WHERE key_name = %s;"
                elif self.db_type == DbType.SQLITE:
                    sql_text = "SELECT value_str FROM configuration WHERE key_name = ?;"
                cursor.execute(sql_text, ("db_version",))
                db_ver = cursor.fetchone()
                if db_ver:
                    db_ver = db_ver[0]
                else:
                    db_ver = "0.0.0"
            except (psycopg2.Error, sqlite3.Error) as e:
                self.connection.rollback()
                db_ver = "0.0.0"
        else:
            return False

        if db_ver >= DB_VERSION[self.db_type]:
            return True
        else:
            print(
                f"Database version {db_ver} is lower than required {DB_VERSION[self.db_type]}. Do you want to update the database? (y/n)")
            if input().lower() in ["y", "yes"]:
                return self.update_db()
            return False

    def change_connection_params(self):
        """Method to change connection parameters."""
        pass


# Connection manager instance
connection_manager = ConnectionManager(DbType.POSTGRES)


# UI functions
def change_db_type():
    """Method to change the database type."""
    while True:
        print("1. Central (PostgreSQL)")
        print("2. Local (SQLite)")
        print("0. Cancel")
        choice = input("Select an option: ").strip().lower()

        if choice in ["0", "cancel"]:
            return
        if choice not in ["1", "2", "central", "local"]:
            print("Invalid choice. Please try again.")
            continue
        elif choice in ["1", "central"]:
            connection_manager.db_type = DbType.POSTGRES
        elif choice in ["2", "local"]:
            connection_manager.db_type = DbType.SQLITE

        connection_manager.connection = connection_manager.connect()

        if not connection_manager.connection:
            print("Failed to connect to the database.")
        else:
            if connection_manager.check_db_version():
                print("Database is up to date.")
            else:
                print("Database update failed.")
        break


def db_settings_screen():
    """Method to display database settings."""
    while True:
        print("="*10, "Database settings:", "="*10)
        print(f"Current database type: {connection_manager.db_type.value}")
        print()
        print("1. Change database type")
        print("2. Change connection parameters (TBI)")
        print("3. Check database version")
        print("0. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            change_db_type()
        elif choice == "2":
            connection_manager.change_connection_params()
        elif choice == "3":
            if connection_manager.check_db_version():
                print("Database is up to date.")
            else:
                print("Database update failed.")
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
