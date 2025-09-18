from src.minigames import *
from src.class_menu import MenuOption, MenuScreen
from src.users.user_service import UserService
from .puzzle_15 import Puzzle15
from .bulls_n_cows import BullsAndCows


def play_bulls_n_cows():
    game = BullsAndCows(UserService.logged_user)
    game.play()


def play_fifteen_puzzle():
    # game = Puzzle15(UserService.logged_user)
    # game.play()

    def load_game():
        # nonlocal game
        game = Puzzle15(UserService.logged_user)
        game.load_game()
        game.play()

    def play_game():
        Puzzle15(UserService.logged_user).play()
        # game.play()

    options = []
    options.append(MenuOption("New game", play_game))
    options.append(MenuOption("Continue game", load_game))
    # options.append(("Records", game.show_records))

    MenuScreen("15 Puzzle", options).show_menu()


############# MENU #################################


def menu_minigames_select():
    """Method to display minigames menu."""
    options = [
        MenuOption("Bulls and Cows", play_bulls_n_cows),
        MenuOption("15 Puzzle", play_fifteen_puzzle)
    ]

    MenuScreen("Minigames", options).show_menu()
