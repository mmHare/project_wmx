
from enum import Enum
import os

from src.database.db_functions import query_select_one, query_upsert
from src.users.class_user import User
from tinydb import TinyDB, Query


class GameMode(Enum):
    NOT_PLAYABLE = 0
    SINGLE = 1
    MULTI = 2
    BOTH = 3


class ScoreRule(Enum):
    ASC = 0  # highscores are higher numbers
    DESC = 1  # highscores are lower numbers


class MiniGame:
    def __init__(self, code, user: User):
        self.code = code
        self.name = ""
        self.description = ""
        self.user = user
        self.game_mode = GameMode.NOT_PLAYABLE
        self.highscore = 0
        self.score_rule = ScoreRule.ASC
        self.times_played = 0
        self.game_data = []

    def play(self):
        pass

    def player_win(self, score, clear_game_data: bool = True):
        self.update_times_played()
        self.update_highscore(score)
        if clear_game_data:
            self.game_data = None
        self.save_game()
        print("You win!")

    def player_loose(self, clear_game_data: bool = True):
        self.update_times_played()
        if clear_game_data:
            self.game_data = None
        self.save_game()
        print("You loose!")

    def player_quits(self):
        self.update_times_played()
        print("Good bye!")

    def update_highscore(self, score: int):
        if self.score_rule == ScoreRule.DESC:
            self.highscore = min(self.highscore, score)
        else:
            self.highscore = max(self.highscore, score)

    def update_times_played(self, times_played: int = None):
        if times_played:
            self.times_played = times_played
        else:
            self.times_played = self.times_played + 1

    def save_game(self, game_data=None):
        if game_data:
            self.game_data = game_data

        try:
            # save score to SQL db
            sql_text = "INSERT INTO minigames_scores (game_code, user_id, highscore, times_played) VALUES (:game_code, :user_id, :highscore, :times_played);"
            params = {
                "game_code": self.code,
                "user_id": self.user.id,
                "highscore": self.highscore,
                "times_played": self.times_played
            }
            query_upsert(sql_text, params, ("game_code", "user_id"))

            # save local gamedata
            data_to_save = {
                "game_code": self.code,
                "user_id": self.user.id,
                "db_kind": self.user.db_kind.value,
                "game_data": self.game_data
            }
            db = TinyDB("./db/saves.json")
            db.insert(data_to_save)
        except Exception as e:
            print(f"Error while saving {self.code} data: {e}")

    def load_game(self):
        try:
            sql_text = "SELECT * FROM minigames_scores WHERE game_code = :game_code AND user_id = :user_id AND deleted = :deleted;"
            params = {
                "game_code": self.code,
                "user_id": self.user.id,
                "deleted": False
            }
            result = query_select_one(sql_text, params, dict_result=True)
            self.highscore = result.get("highscore", 0)
            self.times_played = result.get("times_played", 0)

            if os.path.isfile("./db/saves.json"):
                db = TinyDB("./db/saves.json")
                q_data = Query()
                db_data = db.get(
                    (q_data.game_code == self.code) & (q_data.user_id == self.user.id) & (q_data.db_kind == self.user.db_kind.value))
                if db_data:
                    self.game_data = db_data.get("game_data", None)
        except Exception as e:
            print(f"Error while loading {self.code} data: {e}")

        return self.game_data
