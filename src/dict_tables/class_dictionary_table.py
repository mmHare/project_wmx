"""Class representing the dictionary table."""

from src.users.class_user import User
from src.database.db_functions import *
from src.globals.glob_dicts import *
from src.users.class_user_manager import get_user_manager


user_manager = get_user_manager()


class TableItem:
    def __init__(self, word="", value=""):
        self.id = 0
        self.word = word
        self.value = value


class DictionaryTable:
    def __init__(self, table_name="", columns=["id"]):
        self.table_name = table_name
        self.description = ""
        self.visibility = "private"
        self.created_by = None  # type: User
        self.columns = columns
        self.items = []  # type: list[TableItem]

    @property
    def visibility_int(self):
        return VISIBILITY_ACCESS[self.visibility]

    @property
    def is_public(self):
        return self.visibility_int == ACC_PRIVATE


class DictionaryTableManager:
    def __init__(self):
        # self.dictionary_table = DictionaryTable()
        pass

    def get_visibility_from_int(self, visb: int):
        # temporary, need to find better way
        if visb == 1:
            return ACC_PRIVATE
        else:
            return ACC_PUBLIC

    def get_table_list(self):
        try:
            sql_text = "SELECT * FROM dict_tables;"
            result = query_select(sql_text, dict_result=True)
            tables = []
            for res in result:
                table = DictionaryTable(res["table_name"])
                table.description = res["description"]
                table.visibility = self.get_visibility_from_int(
                    res["visibility"])
                table.created_by = res["created_by"]
                tables.append(table)

        except Exception as e:
            print("Error getting list of tables:", e)
            return None
        return tables

    def create_table(self, table: DictionaryTable):
        tab_name = table.table_name.lower()
        user_id = user_manager.logged_user.id
        try:
            if table.table_name == "":
                raise Exception("No table name.")
            # check if table is recorded
            sql_text = "SELECT id, created_by, visibility FROM dict_tables WHERE table_name = :table_name"
            params = {"table_name": tab_name}
            result = query_select(sql_text, params, dict_result=True)
            if result:
                # test and correct (problem probably with dict result)
                if (result["created_by"] != user_id) and (result["visibility"] == "private"):
                    raise Exception(
                        "Another user created table with the same name.")
                else:
                    raise Exception(
                        f"Table {tab_name.upper()} already exists.")

            # check if table exists even if it is not recorded in dict_tables
            if query_table_exists(tab_name):
                raise Exception(
                    f"Table {tab_name.upper()} already exists. Please contact database administrator for further info.")

            # create table
            if query_create_table(table.table_name, table.columns):
                # insert record to dict_tables
                sql_text = "INSERT INTO dict_tables (table_name, description, visibility, created_by) VALUES (:table_name, :description, :visibility, :created_by)"
                params = {
                    "table_name": table.table_name,
                    "description": table.description,
                    "visibility": table.visibility_int,
                    "created_by": user_id
                }
                query_insert(sql_text, params)

        except Exception as e:
            print("Error creating new table:", e)
            return False
        return True

    def delete_table(self, table: DictionaryTable):
        # Code to delete the dictionary table from the database
        pass

    def load_table(self):
        # Code to load the dictionary table from the database
        table = DictionaryTable()
        return table

    def save_table(self, table: DictionaryTable):
        # Code to save the dictionary table to the database
        pass

    def add_item(self, table: DictionaryTable, item: TableItem):
        pass

    def update_item(self, table: DictionaryTable, item: TableItem):
        pass

    def delete_item(self, table: DictionaryTable, item: TableItem):
        pass


# Instance
_dict_tab_manager = None


def get_dict_tab_manager():
    global _dict_tab_manager
    if _dict_tab_manager is None:
        _dict_tab_manager = DictionaryTableManager()
    return _dict_tab_manager
