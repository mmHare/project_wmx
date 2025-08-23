
CREATE TABLE IF NOT EXISTS public."configuration" (
	id serial4 NOT NULL,
	key_name varchar NOT NULL UNIQUE,
	value_str varchar NULL,
	value_int int4 NULL,
	CONSTRAINT configuration_key_name_key UNIQUE (key_name),
	CONSTRAINT configuration_pk PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS public.users (
	id serial4 NOT NULL,
	"name" varchar NULL,
	surname varchar NULL,
	login varchar NULL,
	deleted bool DEFAULT false NOT NULL,
	"password" varchar NULL,
	user_role int4 NULL,
	ip_address varchar NULL,
	CONSTRAINT users_pk PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.dict_tables(
	id serial4 NOT NULL,
	table_name varchar NOT NULL,
	description varchar NULL,
	visibility int4 NULL,
	owner_id int4 NULL,
	table_name_ref varchar NULL,
	CONSTRAINT dict_tables_pk PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.minigames(
	id serial4 NOT NULL,
	code varchar NOT NULL,
	name varchar NULL,
	description varchar NULL,
	enabled bool DEFAULT true NOT NULL,
	game_mode int4 NULL,
	CONSTRAINT minigames_code UNIQUE (code),
	CONSTRAINT minigames_pk PRIMARY KEY (id)
);