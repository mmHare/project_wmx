"""Database management related functions"""


from src.globals import *
from src.database.connection_manager import get_connection_manager
from src.config.settings_service import get_config_manager


class DatabaseService:
    _connection_manager = get_connection_manager()
    _config_manager = get_config_manager()

    @property
    def is_connected(cls):
        return cls._connection_manager.connection != None

    @classmethod
    def change_db_type(cls):
        """Method to change the database type."""

        print(cls.connected_db_str())
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
            cls._connection_manager.connection = cls._connection_manager.connect(
                DbKind.CENTRAL.value)
        elif choice == 2:
            cls._connection_manager.connection = cls._connection_manager.connect(
                DbKind.LOCAL.value)

        if not cls._connection_manager.connection:
            print("Failed to connect to the database.")
        else:
            if cls._connection_manager.check_db_version():
                # db ok so saving to config
                cls._config_manager.config[CONF_DATABASE][CONF_DB_KIND] = DB_KIND[cls._connection_manager.db_type].value
                cls._config_manager.save_config()
            else:
                print("Database update failed.")
        return True

    @classmethod
    def check_db_version(cls):
        cls._connection_manager.check_db_version()

    @classmethod
    def check_db_connection(cls):
        if cls._connection_manager.connection:
            print("Connected")
        else:
            print("No connection")

    @classmethod
    def reconnect(cls):
        try:
            result = cls._connection_manager.reconnect()
            if result:
                print("Connection success.")
            else:
                print("Connection error.")
        except Exception as e:
            print("Error while reconnecting to database:", e)
        return result

    @classmethod
    def connect(cls):
        cls._connection_manager.connect()
        if cls._connection_manager.connection:
            print("Connection success.")
        else:
            print("Could not connect to database.")

    @classmethod
    def disconnect(cls):
        try:
            print("Closing connection...")
            cls._connection_manager.close_connection()
            if not cls._connection_manager.connection:
                print("Connection closed.")
            else:
                print("Connection was not closed.")
        except Exception as e:
            print("Error while disconnecting:", e)

    @classmethod
    def connected_db_str(cls):
        result = f"Database: {DB_KIND[cls._connection_manager.db_type].value.capitalize()}"
        return result + f" - {bcolors.OKGREEN}Connected{bcolors.ENDC}" if cls._connection_manager.connection else f" - {bcolors.FAIL}Not connected{bcolors.ENDC}"

    @classmethod
    def get_db_kind_connection(cls) -> DbKind:
        return DB_KIND[cls._connection_manager.db_type]

    @classmethod
    def get_api_address(cls):
        return cls._connection_manager.get_api_address()

    # executing queries

    @classmethod
    def query_select(cls, sql_text: str, params: dict = None, dict_result: bool = False):
        return cls._connection_manager.exec_sql_select(sql_text, params, dict_result=dict_result)

    @classmethod
    def query_select_one(cls, sql_text: str, params: dict = None, dict_result: bool = False):
        return cls._connection_manager.exec_sql_select(sql_text, params, fetch_one=True, dict_result=dict_result)

    @classmethod
    def query_insert(cls, sql_text: str, params: dict = None):
        return cls._connection_manager.exec_sql_modify(QueryMode.INSERT, sql_text, params)

    @classmethod
    def query_update(cls, sql_text: str, params: dict = None):
        return cls._connection_manager.exec_sql_modify(QueryMode.UPDATE, sql_text, params)

    @classmethod
    def query_delete(cls, sql_text: str, params: dict = None):
        return cls._connection_manager.exec_sql_modify(QueryMode.DELETE, sql_text, params)

    @classmethod
    def query_upsert(cls, sql_text: str, params: dict = None, key_fields: tuple = None):
        return cls._connection_manager.exec_sql_modify(QueryMode.UPSERT, sql_text, params, key_fields)

    @classmethod
    def query_table_exists(cls, table_name: str) -> bool:
        """Returns True if table with given name exists in the database, False otherwise"""
        return cls._connection_manager.exec_sql_table_exists(table_name)

    @classmethod
    def query_create_table(cls, table_name: str, columns: list):
        """Creates table from given name and column names, PK column 'id' is added automatically.
            Returns True if Table was created.
        """
        return cls._connection_manager.exec_sql_create_table(table_name, columns)
