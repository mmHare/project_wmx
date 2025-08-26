import random

from src.globals.help_functions import clear_screen

from .class_mini_game import GameMode, MiniGame, ScoreRule


class Puzzle15(MiniGame):

    def __init__(self, user=None):
        super().__init__("15_puzzle", user)
        self.name = "15 Puzzle"
        self.game_mode = GameMode.SINGLE
        self.score_rule = ScoreRule.DESC
        self.game_data = dict()
        self.board_solved = [[(i+4*j) for i in range(4)] for j in range(4)]

    def print_board(self, board):
        """Method for printing the board 'tiles'"""
        for row in board:
            print('\t'.join('' if item == 0 else f"[{item}]" for item in row))
        print('\n'+'-'*30)

    def update_board(self, board, action):
        """Method for updating the tiles configuration basing on action movement"""
        def find_index_empty() -> tuple[int, int]:
            for i, row in enumerate(board):
                for j, value in enumerate(row):
                    if value == 0:
                        return i, j

        def move_up():
            y, x = find_index_empty()
            if y < len(board)-1:
                board[y][x], board[y+1][x] = board[y+1][x], board[y][x]

        def move_down():
            y, x = find_index_empty()
            if y > 0:
                board[y][x], board[y-1][x] = board[y-1][x], board[y][x]

        def move_left():
            y, x = find_index_empty()
            if x < len(board[y])-1:
                board[y][x], board[y][x+1] = board[y][x+1], board[y][x]

        def move_right():
            y, x = find_index_empty()
            if x > 0:
                board[y][x], board[y][x-1] = board[y][x-1], board[y][x]

        if action == "w":
            move_up()
        elif action == "s":
            move_down()
        elif action == "a":
            move_left()
        elif action == "d":
            move_right()
        return

    def randomize_board(self):
        # randomizing board into 4x4 matrix
        nums = random.sample(range(16), 16)
        return [nums[i:i+4] for i in range(0, 16, 4)]

    def play(self):
        self.load_game()
        play_board = self.game_data.get("board", None)
        rounds = self.game_data.get("rounds", 1)
        if not play_board:
            play_board = self.randomize_board()
            rounds = 1

        while True:
            clear_screen()
            print("Slide tiles (numbers) to match this configuration:")
            self.print_board(self.board_solved)

            print("BOARD:")
            self.print_board(play_board)
            print(f"Round: {rounds}")
            print("\tW\nA\t\tD\n\tS")
            print("q - Quit, r - Reset\n")
            user_input = input().lower()

            if user_input in ['q']:
                if input("Do you want to save progress? (y/n)\n") == 'y':
                    game_data = {"rounds": rounds, "board": play_board}
                    self.save_game(game_data)
                self.player_quits()
                break
            elif user_input == 'r':
                if input("Do you wish to restart the game? Current progress will be cleared. (y/n)\n") == 'y':
                    play_board = self.randomize_board()
                    rounds = 1
                    game_data = {"rounds": rounds, "board": play_board}
                    self.save_game(game_data)
            elif user_input in ['w', 's', 'a', 'd']:
                self.update_board(play_board, user_input)
                rounds += 1

            if play_board == self.board_solved:
                self.player_win(rounds)
                break
