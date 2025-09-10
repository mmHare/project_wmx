from src.minigames import *
from src.menu_functions import MenuScreen
from src.users.class_user_manager import get_user_manager

user_manager = get_user_manager()


def play_bulls_n_cows():
    game = BullsAndCows(user_manager.logged_user)
    game.play()


def play_fifteen_puzzle():
    # game = Puzzle15(user_manager.logged_user)
    # game.play()

    def load_game():
        # nonlocal game
        game = Puzzle15(user_manager.logged_user)
        game.load_game()
        game.play()

    def play_game():
        Puzzle15(user_manager.logged_user).play()
        # game.play()

    options = []
    options.append(("New game", play_game))
    options.append(("Continue game", load_game))
    # options.append(("Records", game.show_records))

    MenuScreen("15 Puzzle", options).show_menu()


############# MENU #################################


def menu_minigames_select():
    """Method to display minigames menu."""
    options = [
        ("Bulls and Cows", play_bulls_n_cows),
        ("15 Puzzle", play_fifteen_puzzle)
    ]

    MenuScreen("Minigames", options).show_menu()
