"""Dictionary mappings"""

from src.globals import *

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
