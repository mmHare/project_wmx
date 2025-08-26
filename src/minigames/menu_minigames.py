from src.minigames import *
from src.menu_functions import show_menu
from src.users.class_user_manager import get_user_manager

user_manager = get_user_manager()


def get_menu_minigames():
    if user_manager.is_logged:
        return "Minigames", menu_minigames_select
    return None, None


def play_bulls_n_cows():
    game = BullsAndCows(user_manager.logged_user)
    game.play()


def play_fifteen_puzzle():
    game = Puzzle15(user_manager.logged_user)
    game.play()


def menu_minigames_select():
    """Method to display minigames menu."""
    options = [
        ("Bulls and Cows", play_bulls_n_cows),
        ("15 Puzzle", play_fifteen_puzzle)
    ]

    show_menu("Minigames", options)
