"""Class representing the dictionary table."""

from enum import Enum
from src.dict_tables.class_dict_table import DictionaryTable
from src.database import DatabaseService, get_connection_manager
from src.globals.glob_enums import QueryMode, VisAccess
from src.users.user_service import UserService


class TableCheckResult(Enum):
    USABLE = 1         # exists + dict record + visible
    STALE = 2          # dict record exists but table missing
    ORPHAN = 3         # table exists but no dict record
    HIDDEN = 4         # dict record exists, table exists, but not visible
    MISSING = 5        # neither exists


class DictionaryTableManager:
    _connection_manager = get_connection_manager()

    def __init__(self):
        pass

    def get_table_list(self) -> list[DictionaryTable]:
        tables = []
        try:
            sql_text = "SELECT * FROM dict_tables;"
            result = DatabaseService.query_select(sql_text, dict_result=True)

            for res in result:
                table = DictionaryTable(res["table_name"])
                table.id = res["id"]
                table.description = res["description"]
                table.visibility = res["visibility"]
                table.owner_id = res["owner_id"]
                tables.append(table)
        except Exception as e:
            print("Error getting list of tables:", e)
        return tables

    def check_table_status(self, table: DictionaryTable) -> TableCheckResult:
        user_id = UserService.logged_user.id
        if table.table_name == "":
            raise Exception("No table name.")

        # if exist physically
        table_exists = DatabaseService.query_table_exists(
            table.table_name_ref)

        # if exist metadata record
        sql_text = "SELECT id, owner_id, visibility FROM dict_tables WHERE table_name_ref = :table_name_ref;"
        params = {"table_name_ref": table.table_name_ref}
        record = DatabaseService.query_select_one(
            sql_text, params, dict_result=True)

        # --- Step 3: determine status ---
        if table_exists and record:
            if (VisAccess(record["visibility"]) == VisAccess.PUBLIC) or (record["owner_id"] == user_id):
                return TableCheckResult.USABLE
            else:
                return TableCheckResult.HIDDEN
        elif record and not table_exists:
            return TableCheckResult.STALE
        elif table_exists and not record:
            return TableCheckResult.ORPHAN
        else:
            return TableCheckResult.MISSING

    def create_table(self, table: DictionaryTable):
        try:
            # result = self.check_table_exist(table)
            result = self.check_table_status(table)
            if result == TableCheckResult.HIDDEN:
                raise Exception(
                    f"Table '{table.table_name}' was already created by another user.")
            elif result != TableCheckResult.MISSING:
                raise Exception(f"Table '{table.table_name}' already exists.")

            # create table
            if DatabaseService.query_create_table(table.table_name_ref, table.columns):
                # insert record to dict_tables
                sql_text = "INSERT INTO dict_tables (table_name, description, visibility, owner_id, table_name_ref) VALUES (:table_name, :description, :visibility, :owner_id, :table_name_ref);"
                params = {
                    "table_name": table.table_name,
                    "description": table.description,
                    "visibility": int(table.visibility),
                    "owner_id": UserService.logged_user.id,
                    "table_name_ref": table.table_name_ref
                }
                DatabaseService.query_insert(sql_text, params)

            if self.check_table_status(table) != TableCheckResult.USABLE:
                raise Exception(
                    "Partial creation. Please contact database manager for further info.")
        except Exception as e:
            print("Error creating new table:", e)
            return False
        return True

    def delete_table(self, table: DictionaryTable):
        try:
            result = True
            tab_check = self.check_table_status(table)
            if tab_check in [TableCheckResult.MISSING, TableCheckResult.ORPHAN]:
                print(f"There is no table {table.table_name}.")
            elif tab_check == TableCheckResult.HIDDEN:
                print("Only owners can delete their tables.")
            else:
                sql_text = "DELETE FROM dict_tables WHERE table_name_ref = :table_name_ref;"
                params = {"table_name_ref": table.table_name_ref}
                DatabaseService.query_delete(sql_text, params)
                tab_check = self.check_table_status(table)
                if tab_check in [TableCheckResult.USABLE, TableCheckResult.STALE]:
                    print("Could not delete table.")
                    result = False

            if tab_check in [TableCheckResult.ORPHAN]:
                sql_text = f"DROP TABLE {table.table_name_ref};"
                self._connection_manager.exec_sql_modify(
                    QueryMode.DROP, sql_text)
                if self.check_table_status(table) in [TableCheckResult.ORPHAN]:
                    print("Could not drop table.")
                    result = False
        except Exception as e:
            print("Error deleting table:", e)
            return False
        return result

    def load_table(self, table_name) -> DictionaryTable:
        # Code to load the dictionary table from the database
        table = DictionaryTable(table_name)
        try:
            tab_check = self.check_table_status(table)
            if not (tab_check == TableCheckResult.USABLE):
                print("Cannot fetch table data.")
                # TODO: rest of checks and msg prints
                return None
            sql_text = "SELECT * FROM dict_tables WHERE table_name_ref = :table_name_ref;"
            params = {"table_name_ref": table.table_name_ref}
            record = DatabaseService.query_select_one(
                sql_text, params, dict_result=True)
            if record:
                table.id = record["id"]
                table.description = record["description"]
                table.owner_id = record["owner_id"]
                table.visibility = record["visibility"]

                # column names
                table.columns = self._connection_manager.sql_get_table_column_names(
                    table.table_name_ref)

                # table items
                sql_text = f"SELECT * FROM {table.table_name_ref};"
                tab_items = DatabaseService.query_select(
                    sql_text, dict_result=True)
                table.items = tab_items

        except Exception as e:
            print(f"Error fetching table data: {e}")
        return table

    def save_table(self, table: DictionaryTable):
        # Code to save the dictionary table to the database
        pass

    def add_item(self, table: DictionaryTable, item: dict):
        try:

            par_keys = [f":{key}" for key in item.keys()]

            sql_text = f"INSERT INTO {table.table_name_ref} ({','.join(item.keys())}) VALUES ({','.join(par_keys)});"
            params = item
            sql_result = DatabaseService.query_insert(sql_text, params)
            return sql_result > 0
        except Exception as e:
            print("Error while inserting table item:", e)
            return False

    def update_item(self, table: DictionaryTable, item: dict):
        try:
            if item.get("id") > 0:
                set_values = ",".join(
                    [f"{key}={value}" for key, value in item.items()])
                sql_text = F"UPDATE {table.table_name_ref} SET {set_values} WHERE id = {item['id']};"
                DatabaseService.query_update(sql_text)
            else:
                raise ValueError("Incorrect ID value.")
        except Exception as e:
            print("Error while deleting table item:", e)
            return False
        return True

    def delete_item_by_id(self, table: DictionaryTable, item_id: int):
        try:
            if item_id > 0:
                sql_text = F"DELETE FROM {table.table_name_ref} WHERE id = {item_id};"
                DatabaseService.query_delete(sql_text)
            else:
                raise ValueError("Incorrect ID value.")
        except Exception as e:
            print("Error while deleting table item:", e)
            return False
        return True


# Instance
_dict_tab_manager = None


def get_dict_tab_manager():
    global _dict_tab_manager
    if _dict_tab_manager is None:
        _dict_tab_manager = DictionaryTableManager()
    return _dict_tab_manager
