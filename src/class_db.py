'''Database connection module for the project.'''

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3

from src.globals import *
from src.help_functions import *
from src.class_config import config_manager
from src.sql_helper import *


class ConnectionManager:
    """Class to manage database connections and operations."""

    def __init__(self, db_type: DbType = DbType.NONE):
        self.db_type = db_type
        self.connection = None

    def __del__(self):
        self.close_connection()

    @property
    def is_local(self):
        return self.db_type == DbType.SQLITE

    @property
    def is_central(self):
        return self.db_type == DbType.POSTGRES

    @property
    def db_cursor(self):
        """Database cursor property."""
        if self.connection is None:
            raise Exception("Database connection is not established.")
        else:
            return self.connection.cursor()

    @property
    def db_cursor_dict(self):
        """Returns a cursor with dictionary-like access."""
        if self.db_type == DbType.POSTGRES:
            return self.connection.cursor(cursor_factory=RealDictCursor)
        else:
            raise Exception(
                "Dictionary cursor is only available for PostgreSQL.")

    def connect(self):
        self.close_connection()
        # central or local
        db_kind = config_manager.config[CONF_DATABASE][CONF_DB_KIND]
        self.db_type = DB_TYPE[DbKind(db_kind)]

        db_config = config_manager.config[CONF_DATABASE]
        try:
            if self.db_type == DbType.POSTGRES:
                db_config = db_config[CONF_DB_CENTRAL]
                if all(key in db_config for key in [
                        CONF_DB_C_NAME, CONF_DB_C_USER, CONF_DB_C_PASS,
                        CONF_DB_C_HOST, CONF_DB_C_PORT]):

                    connection = psycopg2.connect(
                        database=db_config[CONF_DB_C_NAME],
                        user=decrypt_data(db_config[CONF_DB_C_USER]),
                        password=decrypt_data(db_config[CONF_DB_C_PASS]),
                        host=db_config[CONF_DB_C_HOST],
                        port=db_config[CONF_DB_C_PORT]
                    )
                    return connection
                else:
                    print("Database configuration is incomplete. Verify settings.")
                    return None
            elif self.db_type == DbType.SQLITE:
                db_config = db_config[CONF_DB_LOCAL]
                if not os.path.exists(db_config[CONF_DB_L_PATH]):
                    if input("Database file not found. Do you want to create it? (y/n): ").lower() != 'y':
                        return None
                    else:
                        os.makedirs(db_config[CONF_DB_L_PATH], exist_ok=True)
                connection = sqlite3.connect(
                    db_config[CONF_DB_L_PATH] + "/" + db_config[CONF_DB_L_NAME])
                return connection
            else:
                return None
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def reconnect(self):
        self.connection = self.connect()
        if not self.connection:
            return False
        else:
            return True

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
        sql_text = "INSERT INTO configuration (key_name, value_str) VALUES (:conf_key_in, :version_in)"
        key_fields = ("key_name")
        params = {"conf_key_in": "db_version", "version_in": version}
        self.query_execute(QueryMode.UPSERT, sql_text,
                           params, key_fields=key_fields)

    def check_db_version(self):
        sql_text = "SELECT value_str FROM configuration WHERE key_name = :key_in;"
        params = {"key_in": "db_version"}
        db_ver = self.query_execute(
            QueryMode.SELECT, sql_text, params, fetch_one=True)
        if db_ver:
            db_ver = db_ver[0]
        else:
            db_ver = "0.0.0"

        if db_ver >= DB_VERSION[self.db_type]:
            return True
        else:
            print(
                f"Database version {db_ver} is lower than required {DB_VERSION[self.db_type]}. Do you want to update the database? (y/n)")
            if input().lower() in ["y", "yes"]:
                return self.update_db()
            return False

    def query_execute(self, mode: str, sql_text: str, params: dict = None, key_fields: tuple = None, fetch_one: bool = False):
        return query_helper(self.connection, self.db_type, mode, sql_text, params, key_fields, fetch_one)


# Global instance
connection_manager = ConnectionManager()
