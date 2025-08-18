"""Database connection module for the project."""

import os
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3

from src.globals import *
from src.globals.help_functions import decrypt_data
from .sql_helper import query_select, query_modify
from src.config.class_config import get_config_manager

config_manager = get_config_manager()


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

    def connect(self, db_kind=None):
        self.close_connection()
        # central or local
        if db_kind is None:
            db_kind = config_manager.config[CONF_DATABASE][CONF_DB_KIND]
        self.db_type = DB_TYPE[DbKind(db_kind)]

        db_config = config_manager.config[CONF_DATABASE]
        try:
            if self.db_type == DbType.POSTGRES:
                db_config = db_config[CONF_DB_CENTRAL]
                if all(key in db_config for key in [
                        CONF_DB_C_NAME, CONF_DB_C_USER, CONF_DB_C_PASS,
                        CONF_DB_C_HOST, CONF_DB_C_PORT]):

                    self.connection = psycopg2.connect(
                        database=db_config[CONF_DB_C_NAME],
                        user=decrypt_data(db_config[CONF_DB_C_USER]),
                        password=decrypt_data(db_config[CONF_DB_C_PASS]),
                        host=db_config[CONF_DB_C_HOST],
                        port=db_config[CONF_DB_C_PORT]
                    )
                else:
                    print("Database configuration is incomplete. Verify settings.")
                    return None
            elif self.db_type == DbType.SQLITE:
                db_config = db_config[CONF_DB_LOCAL]

                db_path = os.path.join(
                    db_config[CONF_DB_L_PATH], db_config[CONF_DB_L_NAME])

                is_new = not os.path.isfile(db_path)

                if is_new:
                    if input(f"Database file '{db_config[CONF_DB_L_NAME]}' not found. Do you want to create it? (y/n): ").lower() != 'y':
                        return None
                    else:
                        os.makedirs(db_config[CONF_DB_L_PATH], exist_ok=True)

                self.connection = sqlite3.connect(db_path)
                if is_new:
                    self.update_db()
            else:
                return None

            return self.connection
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def reconnect(self):
        self.connection = self.connect()
        if self.connection:
            self.check_db_version()
            return True
        else:
            return False

    def update_db(self):
        """Method to update the database schema."""
        if not self.connection:
            return False

        cursor = self.db_cursor
        sql_path = Path(__file__).parent / "sql" / \
            self.db_type.value / "schema" / "create_tables.sql"

        with open(sql_path, "r", encoding="utf-8") as file:
            sql = " ".join(file.readlines())

        try:
            if self.db_type == DbType.POSTGRES:
                cursor.execute(sql)
            elif self.db_type == DbType.SQLITE:
                for statement in sql.split(';'):
                    if statement.strip():
                        cursor.execute(statement)
            self.connection.commit()
        except Exception as e:
            print(f"Error ocurred during update: {e}")
            self.connection.rollback()
            return False

        try:
            self.set_db_version(DB_VERSION[self.db_type])
        except Exception as e:
            print(f"Error setting database version: {e}")
            return False
        print("Database updated successfully.")
        return True

    def set_db_version(self, version: str):
        """Method to set the database version."""
        key_fields = ("key_name",)
        params = {"conf_key_in": "db_version", "version_in": version}
        sql_text = "INSERT INTO configuration(key_name, value_str) VALUES(:conf_key_in, :version_in)"

        self.exec_sql_modify(QueryMode.UPSERT, sql_text,
                             params, key_fields=key_fields)

    def check_db_version(self):
        sql_text = "SELECT value_str FROM configuration WHERE key_name = :key_in;"
        params = {"key_in": "db_version"}

        try:
            db_ver = self.exec_sql_select(sql_text, params, fetch_one=True)
        except Exception as e:
            print("Error checking database version:", e)
            return False

        if db_ver:
            db_ver = db_ver[0]
        else:
            db_ver = "0.0.0"

        if db_ver >= DB_VERSION[self.db_type]:
            print(f"Database is up to date. Version {db_ver}")
            return True
        else:
            print(
                f"Database version {db_ver} is lower than required {DB_VERSION[self.db_type]}. Do you want to update the database? (y/n)")
            if input().lower() in ["y", "yes"]:
                return self.update_db()
            return False

    def exec_sql_table_exists(self, table_name: str) -> bool:
        table_name = table_name.lower()
        if self.db_type == DbType.POSTGRES:
            sql_text = f"SELECT to_regclass('public.{table_name}') IS NOT NULL;"
        elif self.db_type == DbType.SQLITE:
            sql_text = f"SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type='table' AND name='{table_name}')"
        else:
            raise TypeError("Incorrect database type")

        result = self.exec_sql_select(sql_text, fetch_one=True)
        return bool(result[0])

    def exec_sql_create_table(self, table_name: str, columns: list) -> bool:
        """Creates table from given name and column names (right now only str handled), PK column 'id' is added automatically.
            Returns True if Table was created.
        """
        if self.db_type not in [DbType.POSTGRES, DbType.SQLITE]:
            raise TypeError("Incorrect database type")

        # preparing data
        tab_name = table_name.lower()
        if self.db_type == DbType.POSTGRES:  # postgres format
            id_column = "id serial4 NOT NULL"
            pk_line = f"CONSTRAINT {tab_name}_pk PRIMARY KEY(id)"
            tab_name = "public." + tab_name
            type_name = "varchar"
        elif self.db_type == DbType.SQLITE:
            id_column = "id INTEGER PRIMARY KEY AUTOINCREMENT"
            type_name = "TEXT"

        reserved_sql_names = ["user", "name", "password",
                              "order", "group", "key", "value", "date"]
        column_names = [
            f"'{col}'" if col in reserved_sql_names else col for col in set(columns) if col != "id"]

        column_lines = [id_column] + \
            [f"{col} {type_name}" for col in column_names]
        if self.db_type == DbType.POSTGRES:
            column_lines.append(pk_line)

        sql_text = f"CREATE TABLE {tab_name} ( " + \
            ', '.join(column_lines) + ");"

        cursor = self.db_cursor
        try:
            cursor.execute(sql_text)
            self.connection.commit()
        except:
            self.connection.rollback()
            raise

        return self.exec_sql_table_exists(table_name)

    def exec_sql_select(self, sql_text: str, params: dict = None, fetch_one: bool = False, dict_result: bool = False):
        return query_select(self.connection, self.db_type, sql_text, params, fetch_one, dict_result)

    def exec_sql_modify(self, mode: QueryMode, sql_text: str, params: dict = None, key_fields: tuple = None):
        return query_modify(self.connection, self.db_type,
                            mode, sql_text, params, key_fields)


# Instance
_connection_manager = None


def get_connection_manager():
    global _connection_manager
    if _connection_manager is None:
        _connection_manager = ConnectionManager()
    return _connection_manager
