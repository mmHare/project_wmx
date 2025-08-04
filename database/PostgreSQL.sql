-- public.users definition

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	id serial4 NOT NULL,
	"name" varchar NULL,
	surname varchar NULL,
	login varchar NULL,
	deleted bool DEFAULT false NOT NULL,
	"password" varchar NULL,
	CONSTRAINT users_pk PRIMARY KEY (id)
);