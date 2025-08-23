
CREATE TABLE IF NOT EXISTS bulls_n_cows(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	player_id INTEGER,
	high_score INTEGER,
	times_played INTEGER
);

INSERT INTO minigames (code, name, description, game_mode) 
	VALUES ('bulls_n_cows', 'Bulls and Cows', 'Game of Bulls and Cows', 1) 
	ON CONFLICT (code) DO NOTHING;