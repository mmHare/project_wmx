from enum import Enum


class DbType(Enum):
    NONE = "none"
    POSTGRES = "postgres"
    SQLITE = "sqlite"


# słownik z wersjami bazy danych
DB_VERSION = {
    DbType.POSTGRES: "1.0.0",
    DbType.SQLITE: "1.0.0"
}
