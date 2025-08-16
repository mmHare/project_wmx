"""Enums and dictionaries used globally"""


from enum import Enum


class DbKind(Enum):
    NONE = "none"
    CENTRAL = "central"
    LOCAL = "local"


class DbType(Enum):
    NONE = "none"
    POSTGRES = "postgres"
    SQLITE = "sqlite"


class QueryMode(Enum):
    SELECT = "select"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    UPSERT = "upsert"


class UserRole(Enum):
    NONE = 0
    ADMIN = 1
    USER = 2


# dictionary DB kind <-> DB type
DB_TYPE = {
    DbKind.NONE: DbType.NONE,
    DbKind.CENTRAL: DbType.POSTGRES,
    DbKind.LOCAL: DbType.SQLITE
}
DB_KIND = {v: k for k, v in DB_TYPE.items()}  # reverse to DB_TYPE

# dictionary with DB versions
DB_VERSION = {
    DbType.POSTGRES: "1.0.0",
    DbType.SQLITE: "1.0.0"
}
