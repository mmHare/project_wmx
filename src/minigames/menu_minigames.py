from src.minigames import bulls_n_cows, fifteen_puzzle
from src.menu_functions import show_menu
from src.users import user_manager


def get_menu_minigames():
    if user_manager.is_logged:
        return "Minigames", menu_minigames_select
    return None, None


def menu_minigames_select():
    """Method to display minigames menu."""
    options = [
        ("Bulls and Cows", bulls_n_cows),
        ("15 Puzzle", fifteen_puzzle)
    ]

    show_menu("Minigames", options)
