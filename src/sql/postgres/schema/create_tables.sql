
CREATE TABLE IF NOT EXISTS public."configuration" (
	id serial4 NOT NULL,
	key_name varchar NOT NULL UNIQUE,
	value_str varchar NULL,
	value_int int4 NULL,
	CONSTRAINT configuration_pk PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS public.users (
	id serial4 NOT NULL,
	"name" varchar NULL,
	surname varchar NULL,
	login varchar NULL,
	deleted bool DEFAULT false NOT NULL,
	"password" varchar NULL,
	user_role varchar NULL,
	ip_address varchar NULL,
	CONSTRAINT users_pk PRIMARY KEY (id)
);