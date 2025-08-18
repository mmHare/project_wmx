"""Dictionary mappings"""

from .glob_enums import DbKind, DbType
from .glob_constants import *

# dictionary DB kind <-> DB type
DB_TYPE = {
    DbKind.NONE: DbType.NONE,
    DbKind.CENTRAL: DbType.POSTGRES,
    DbKind.LOCAL: DbType.SQLITE
}

DB_KIND = {v: k for k, v in DB_TYPE.items()}  # reverse to DB_TYPE

# dictionary with DB versions
DB_VERSION = {
    DbType.POSTGRES: "1.0.1",
    DbType.SQLITE: "1.0.1"
}

VISIBILITY_ACCESS = {
    ACC_PRIVATE: 1,
    ACC_PUBLIC: 2
}
