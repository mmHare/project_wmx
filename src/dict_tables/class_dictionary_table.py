"""Class representing the dictionary table."""

from src.users.class_user import User


class DictionaryTable:
    def __init__(self):
        self.table_name = "dictionary"
        self.visibility = "private"
        self.description = "Dictionary of words and their definitions"
        self.created_by = User()
        self.columns = ["id", "word", "definition"]
