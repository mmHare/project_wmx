
CREATE TABLE IF NOT EXISTS configuration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_name TEXT UNIQUE NOT NULL,
    value_str TEXT,
    value_int INTEGER
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT,
    surname TEXT,
    login TEXT,
    deleted INTEGER DEFAULT 0 NOT NULL,
    "password" TEXT,
    user_role INTEGER,
    ip_address TEXT
);

CREATE TABLE IF NOT EXISTS dict_tables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT,
    description TEXT,
    visibility INTEGER,
    created_by INTEGER
    table_name_ref TEXT,
);