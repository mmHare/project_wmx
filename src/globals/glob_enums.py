"""Enums used globally"""

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
