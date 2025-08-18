"""Class representing the dictionary table."""

from src.users.class_user import User


class TableItem:
    def __init__(self, word, value):
        self.word = word
        self.value = value


class DictionaryTable:
    def __init__(self):
        self.table_name = "dictionary"
        self.description = "Dictionary of words and their values"
        self.visibility = "private"
        self.created_by = None  # type: User
        self.columns = ["id", "word", "value"]
        self.items = []  # type: list[TableItem]


class DictionaryTableManager:
    def __init__(self):
        # self.dictionary_table = DictionaryTable()
        pass

    def get_table_list(self):
        # Code to get the list of all dictionary tables
        tables = []
        return tables

    def create_table(self, table: DictionaryTable):
        # Code to create the dictionary table in the database
        pass

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
