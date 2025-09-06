
CREATE TABLE IF NOT EXISTS configuration (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    key_name  TEXT UNIQUE NOT NULL,
    value_str TEXT,
    value_int INTEGER
);

CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    surname     TEXT NOT NULL,
    login       TEXT NOT NULL UNIQUE,
    password    TEXT NOT NULL,
    user_role   INTEGER NOT NULL,
    ip_address  VARCHAR(45), 
    deleted_at  DATETIME DEFAULT NULL,
    guid        TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dict_tables (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name     TEXT NOT NULL UNIQUE,
    description    TEXT,
    visibility     INTEGER,
    owner_id       INTEGER,
    table_name_ref TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS minigames_scores (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    game_code    TEXT NOT NULL,
    user_id      INTEGER NOT NULL,
    highscore    INTEGER,
    times_played INTEGER,
    deleted_at   DATETIME DEFAULT NULL,
    CONSTRAINT minigames_scores_unique_game_user UNIQUE (game_code, user_id)
);
