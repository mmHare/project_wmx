'''Database connection module for the project.'''

import enum
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3


class DbType(enum.Enum):
    NONE = "none"
    POSTGRES = "postgres"
    SQLITE = "sqlite"


class ConnectionManager:
    """Klasa do zarządzania połączeniem z bazą danych."""

    def __init__(self, db_type: DbType = DbType.POSTGRES):
        self.db_type = db_type
        self.connection = None
        self.connection = self.connect()
        if not self.connection:
            raise Exception("Failed to connect to the database.")
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    @property
    def db_cursor(self):
        """Kursor bazy danych"""
        if self.connection is None:
            raise Exception("Database connection is not established.")
        return self.cursor

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

                connection = sqlite3.connect("project_db.sqlite")
                return connection
            else:
                return None
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def close_connection(self):
        if self.connection:
            self.connection.close()
