"""Database management related functions"""


from src.globals import *
from src.database.class_connection_manager import get_connection_manager
from src.config.config_functions import get_config_manager

connection_manager = get_connection_manager()
config_manager = get_config_manager()


def change_db_type():
    """Method to change the database type."""

    print(connected_db_str())
    print("Select database type:")
    print("1. Central (PostgreSQL)")
    print("2. Local (SQLite)")
    print("0. Cancel")
    choice = input("Select an option: ").strip().lower()

    if choice not in ["1", "2", "0"]:
        print("Invalid choice.")
        return

    choice = int(choice)

    if choice == 0:
        return False
    elif choice == 1:
        connection_manager.connection = connection_manager.connect(
            DbKind.CENTRAL.value)
    elif choice == 2:
        connection_manager.connection = connection_manager.connect(
            DbKind.LOCAL.value)

    if not connection_manager.connection:
        print("Failed to connect to the database.")
    else:
        if connection_manager.check_db_version():
            # db ok so saving to config
            config_manager.config[CONF_DATABASE][CONF_DB_KIND] = DB_KIND[connection_manager.db_type].value
            config_manager.save_config()
        else:
            print("Database update failed.")
    return True


def check_db_version():
    connection_manager.check_db_version()


def check_db_connection():
    if connection_manager.connection:
        print("Connected")
    else:
        print("No connection")


def db_reconnect():
    try:
        result = connection_manager.reconnect()
        if result:
            print("Connection success.")
        else:
            print("Connection error.")
    except Exception as e:
        print("Error while reconnecting to database:", e)
    return result


def db_connect():
    connection_manager.connect()
    if connection_manager.connection:
        print("Connection success.")
    else:
        print("Could not connect to database.")


def db_disconnect():
    try:
        print("Closing connection...")
        connection_manager.close_connection()
        if not connection_manager.connection:
            print("Connection closed.")
        else:
            print("Connection was not closed.")
    except Exception as e:
        print("Error while disconnecting:", e)


def connected_db_str():
    result = f"Database: {DB_KIND[connection_manager.db_type].value.capitalize()}"
    return result + f" - {bcolors.OKGREEN}Connected{bcolors.ENDC}" if connection_manager.connection else f" - {bcolors.FAIL}Not connected{bcolors.ENDC}"


def get_db_kind_connection() -> DbKind:
    return DB_KIND[connection_manager.db_type]


# executing queries
def query_select(sql_text: str, params: dict = None, dict_result: bool = False):
    return connection_manager.exec_sql_select(sql_text, params, dict_result=dict_result)


def query_select_one(sql_text: str, params: dict = None, dict_result: bool = False):
    return connection_manager.exec_sql_select(sql_text, params, fetch_one=True, dict_result=dict_result)


def query_insert(sql_text: str, params: dict = None):
    return connection_manager.exec_sql_modify(QueryMode.INSERT, sql_text, params)


def query_update(sql_text: str, params: dict = None):
    return connection_manager.exec_sql_modify(QueryMode.UPDATE, sql_text, params)


def query_delete(sql_text: str, params: dict = None):
    return connection_manager.exec_sql_modify(QueryMode.DELETE, sql_text, params)


def query_upsert(sql_text: str, params: dict = None, key_fields: tuple = None):
    return connection_manager.exec_sql_modify(QueryMode.UPSERT, sql_text, params, key_fields)


def query_table_exists(table_name: str) -> bool:
    """Returns True if table with given name exists in the database, False otherwise"""
    return connection_manager.exec_sql_table_exists(table_name)


def query_create_table(table_name: str, columns: list):
    """Creates table from given name and column names, PK column 'id' is added automatically.
        Returns True if Table was created.
    """
    return connection_manager.exec_sql_create_table(table_name, columns)
