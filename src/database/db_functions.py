"""Database management related functions"""


from .class_db import connection_manager
from src.config import config_manager
from src.globals import *


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
                # db ok so saving to config
                config_manager.config[CONF_DB_KIND] = DB_KIND[connection_manager.db_type]
                config_manager.save_config()
            else:
                print("Database update failed.")
        break


def check_db_version():
    if connection_manager.check_db_version():
        print("Database is up to date.")
    else:
        print("Database update failed.")


def check_db_connection():
    if connection_manager.connection:
        print("Connected")
    else:
        print("No connection")


def db_reconnect():
    if connection_manager.reconnect():
        print("Connection success")
    else:
        print("Connection error")


# executing queries
def query_select(sql_text: str, params: dict = None, fetch_one: bool = False, dict_result: bool = False):
    return connection_manager.query_execute(QueryMode.SELECT, sql_text, params, fetch_one=fetch_one, dict_result=dict_result)


def query_select_one(sql_text: str, params: dict = None, dict_result: bool = False):
    return connection_manager.query_execute(QueryMode.SELECT, sql_text, params, fetch_one=True, dict_result=dict_result)


def query_insert(sql_text: str, params: dict = None):
    return connection_manager.query_execute(QueryMode.INSERT, sql_text, params)


def query_update(sql_text: str, params: dict = None):
    return connection_manager.query_execute(QueryMode.UPDATE, sql_text, params)


def query_delete(sql_text: str, params: dict = None):
    return connection_manager.query_execute(QueryMode.DELETE, sql_text, params)


def query_upsert(sql_text: str, params: dict = None, key_fields: tuple = None):
    return connection_manager.query_execute(QueryMode.UPSERT, sql_text, params, key_fields)
