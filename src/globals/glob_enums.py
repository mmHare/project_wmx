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
    DROP = "drop"


class UserRole(Enum):
    NONE = 0
    ADMIN = 1
    USER = 2


# Visibility/Accessibility
class VisAccess(Enum):
    PRIVATE = 1
    PUBLIC = 2

    def __str__(self):
        """Display as string value"""
        return self.name.lower()

    def __int__(self):
        """Return int value"""
        return self.value

    @classmethod
    def from_str(cls, value: str):
        """Convert from string to enum."""
        return cls[value.upper()]

    @classmethod
    def from_int(cls, value: int):
        """Convert from integer value to enum."""
        return cls(value)

    def to_int(self):
        """Convert enum to integer."""
        return int(self)
