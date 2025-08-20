"""Class of Dictionary Table and its items"""


from src.globals.glob_enums import VisAccess


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
        self.owner_id = None  # id of user who created table
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
