
CREATE TABLE IF NOT EXISTS public."configuration" (
	id         serial4 NOT NULL,
	key_name   varchar NOT NULL,
	value_str  varchar NULL,
	value_int  int4 NULL,
	CONSTRAINT configuration_key_name_uq UNIQUE (key_name),
	CONSTRAINT configuration_pk PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS public.users (
	id          serial4 NOT NULL,
	name        varchar NOT NULL,
	surname     varchar NOT NULL,
	login       varchar NOT NULL,
	password    varchar NOT NULL,
	user_role   int4 NOT NULL,
	ip_address  varchar NULL,
	deleted_at  timestamp WITH TIME ZONE DEFAULT NULL,
	guid        varchar NOT NULL,
	CONSTRAINT users_login_uq UNIQUE (login),
	CONSTRAINT users_guid_uq UNIQUE (guid),
	CONSTRAINT users_pk PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.dict_tables(
	id             serial4 NOT NULL,
	table_name     varchar NOT NULL,
	description    varchar NULL,
	visibility     int4 NULL,
	owner_id       int4 NULL,
	table_name_ref varchar NOT NULL,
	CONSTRAINT dict_tables_table_name_uq UNIQUE (table_name),
	CONSTRAINT dict_tables_pk PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.minigames_scores (
	id           serial4 NOT NULL,
	game_code    varchar NOT NULL,
	user_id      int4 NOT NULL,
	highscore    int4 NULL,
	times_played int4 NULL,
	deleted_at  timestamp WITH TIME ZONE DEFAULT NULL,
	CONSTRAINT minigames_scores_game_user_uq UNIQUE (game_code, user_id),
	CONSTRAINT minigames_scores_pk PRIMARY KEY (id)
);