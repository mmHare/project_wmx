
CREATE TABLE IF NOT EXISTS public.bulls_n_cows(
	id serial4 NOT NULL,
	player_id int4 NULL,
	high_score int4 NULL,
	times_played int4 NULL,
	CONSTRAINT bulls_n_cows_pk PRIMARY KEY (id)
);

INSERT INTO public.minigames (code, name, description, game_mode) 
	VALUES ('bulls_n_cows', 'Bulls and Cows', 'Game of Bulls and Cows', 1) 
	ON CONFLICT (code) DO NOTHING;