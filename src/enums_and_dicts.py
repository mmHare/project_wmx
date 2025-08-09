from enum import Enum


class DbKind(Enum):
    NONE = "none"
    CENTRAL = "central"
    LOCAL = "local"


class DbType(Enum):
    NONE = "none"
    POSTGRES = "postgres"
    SQLITE = "sqlite"


# dictionary with DB versions
DB_VERSION = {
    DbType.POSTGRES: "1.0.0",
    DbType.SQLITE: "1.0.0"
}

# dictionary DB kind <-> DB type
DB_TYPE = {
    DbKind.NONE: DbType.NONE,
    DbKind.CENTRAL: DbType.POSTGRES,
    DbKind.LOCAL: DbType.SQLITE
}
