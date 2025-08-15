
CREATE TABLE IF NOT EXISTS configuration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_name TEXT NOT NULL,
    value_str TEXT,
    value_int INTEGER
);

-- Table: users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT,
    surname TEXT,
    login TEXT,
    deleted INTEGER DEFAULT 0 NOT NULL,
    "password" TEXT,
    user_role TEXT,
    ip_address TEXT
);
