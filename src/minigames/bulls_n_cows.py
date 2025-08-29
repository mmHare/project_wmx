import random

from src.globals.help_functions import clear_screen

from .class_mini_game import MiniGame, GameMode


class BullsAndCows(MiniGame):
    def __init__(self, user=None):
        super().__init__("bulls_n_cows", user)
        self.code = "bulls_n_cows"
        self.name = "Bulls and Cows"
        self.game_mode = GameMode.SINGLE
        self.has_local_save = False
        self.tries_limit = 25

    def new_game(self):
        self.secret_number = random.randint(1000, 9999)
        self.tries_left = self.tries_limit
        clear_screen()
        print("Bulls and Cows")
        print("4-digit secret number has been generated. Try to guess it.")
        print("Bulls - digits exist in secret number")
        print("Cows - digits match the secret number")

    def check_guess(self, number: str) -> tuple[int, int]:
        try:
            secret_number_str = str(self.secret_number)

            unique_digits = set([n for n in number])
            bulls = sum([min(number.count(digit), secret_number_str.count(digit))
                        for digit in unique_digits])
            cows = sum([1 for i in range(len(number)) if (
                number[i] == secret_number_str[i])])
        except Exception as e:
            print(f"{self.code} - Error on check guess: {e}")
            return 0, 0
        return bulls, cows

    def play(self):
        self.new_game()

        while True:
            print(f"Tries left: {self.tries_left}")
            user_guess = input("Enter number (or q to quit):\n")
            if user_guess == "q":
                self.player_quits()
                break

            if (not user_guess.isdigit()) or (len(user_guess) != 4):
                print("Please enter 4-digit number.")
                continue

            bulls, cows = self.check_guess(user_guess)
            print(f"Bulls: {bulls}, Cows: {cows}")

            if cows == len(str(self.secret_number)):
                self.player_win(self.tries_left)
                if input("Do you want to start new game? 'y' to confirm\n") == 'y':
                    self.new_game()
                else:
                    break
            else:
                self.tries_left -= 1

            if self.tries_left <= 0:
                self.player_loose()
                if input("Do you want to start new game? 'y' to confirm\n") == 'y':
                    self.new_game()
                else:
                    break
