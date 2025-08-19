"""Class representing the dictionary table."""

from src.users.class_user import User
from src.database.db_functions import *
# from src.globals.glob_dicts import *
from src.users.class_user_manager import get_user_manager


user_manager = get_user_manager()


class TableItem:
    def __init__(self, word="", value=""):
        self.id = 0
        self.word = word
        self.value = value


class DictionaryTable:
    def __init__(self, table_name="", columns=["id"]):
        self.id = 0
        self._table_name = table_name
        self.description = ""
        self._visibility = VisAccess.PRIVATE  # private/public
        self.created_by = None  # type: User
        self.columns = columns
        self.items = []  # type: list[TableItem]

    @property
    def visibility(self) -> VisAccess:
        return self._visibility

    @property
    def visibility_int(self):
        return VisAccess.to_int(self._visibility)

    @visibility.setter
    def visibility(self, value):
        if isinstance(value, str):
            self._visibility = VisAccess.from_str(value)
        elif isinstance(value, int):
            self._visibility = VisAccess(value)
        elif isinstance(value, VisAccess):
            self._visibility = value
        else:
            raise ValueError("visibility must be str, int or VisAccess")

    @property
    def table_name(self):
        return self._table_name.lower()

    @property
    def table_name_ref(self):
        return "ut_" + self._table_name.lower().removeprefix("ut_")

    @table_name.setter
    def table_name(self, value: str):
        self._table_name = value.lower().removeprefix("ut_")

    @property
    def is_public(self) -> bool:
        return self._visibility == VisAccess.PUBLIC


class DictionaryTableManager:
    def __init__(self):
        # self.dictionary_table = DictionaryTable()
        pass

    def get_table_list(self) -> list[DictionaryTable]:
        tables = []
        try:
            sql_text = "SELECT * FROM dict_tables;"
            result = query_select(sql_text, dict_result=True)

            for res in result:
                table = DictionaryTable(res["table_name"])
                table.id = res["id"]
                table.description = res["description"]
                table.visibility = res["visibility"]
                table.created_by = res["created_by"]
                tables.append(table)
        except Exception as e:
            print("Error getting list of tables:", e)
        return tables

    def check_table_exist(self, table: DictionaryTable) -> int:
        user_id = user_manager.logged_user.id
        result = 0  # TODO: work out some other solution
        if table.table_name == "":
            raise Exception("No table name.")
        # check if table is recorded
        sql_text = "SELECT id, created_by, visibility FROM dict_tables WHERE table_name_ref = :table_name_ref;"
        params = {"table_name_ref": table.table_name_ref}
        query_res = query_select_one(sql_text, params, dict_result=True)
        if query_res:
            if (query_res["created_by"] != user_id) and (query_res["visibility"] == "private"):
                result += 2  # created by another user
            result += 1  # exists

        # check if table exists even if it is not recorded in dict_tables
        if query_table_exists(table.table_name_ref):
            result += 4
        return result

    def create_table(self, table: DictionaryTable):
        try:
            result = self.check_table_exist(table)
            if result in [2, 6]:
                print(
                    f"Table '{table.table_name}' was already created by another user.")
                return False
            elif result in [1, 5]:
                print(f"Table '{table.table_name}' already exists.")
                return False

            # create table
            if query_create_table(table.table_name_ref, table.columns):
                # insert record to dict_tables
                sql_text = "INSERT INTO dict_tables (table_name, description, visibility, created_by, table_name_ref) VALUES (:table_name, :description, :visibility, :created_by, :table_name_ref);"
                params = {
                    "table_name": table.table_name,
                    "description": table.description,
                    "visibility": int(table.visibility),
                    "created_by": user_manager.logged_user.id,
                    "table_name_ref": table.table_name_ref
                }
                query_insert(sql_text, params)

        except Exception as e:
            print("Error creating new table:", e)
            return False
        return True

    def delete_table(self, table: DictionaryTable):
        try:
            user_id = user_manager.logged_user.id
            sql_text = "SELECT created_by, visibility FROM dict_tables WHERE table_name_ref = :table_name_ref;"
            params = {"table_name_ref": table.table_name_ref}
            query_res = query_select_one(sql_text, params, dict_result=True)
            if not query_res:
                raise Exception(f"Table {table.table_name} does not exist.")
            elif (query_res["created_by"] != user_id):
                raise Exception("Only owners can delete their tables.")

            if self.check_table_exist(table) > 4:
                sql_text = f"DROP TABLE {table.table_name_ref};"
                connection_manager.exec_sql_modify(QueryMode.DROP, sql_text)

                if self.check_table_exist(table) > 4:
                    raise Exception("Could not drop table.")

            sql_text = "DELETE FROM dict_tables WHERE table_name_ref = :table_name_ref;"
            params = {"table_name_ref": table.table_name_ref}
            query_delete(sql_text, params)
            if self.check_table_exist(table):
                raise Exception("Could not delete table record.")
        except Exception as e:
            print("Error deleting table:", e)
            return False
        return True

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
