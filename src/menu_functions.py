"""Menu showing the available options."""

import types

from src.help_functions import *


def show_menu(title, options: list, info_top=None, info_bottom=None):
    """Display a menu with the given title and options.

    Args:
        title (str): The title of the menu.
        options (list): A list of tuples containing option descriptions and their corresponding functions. Or function returning such tuple.
        info_top (optional): Additional information to display at the top of the menu (str or func returning str). Defaults to None.
        info_bottom (optional): Additional information to display at the bottom of the menu (str or func returning str). Defaults to None.
    """
    if len(options) == 0:
        return

    while True:
        clear_screen()
        menu_options = []
        print("=" * 10, title.upper(), "=" * 10)

        if info_top:
            print(info_top() if callable(info_top) else info_top)
            print()

        for option in options:
            try:
                if type(option) == types.FunctionType:
                    desc, func = option()
                elif type(option) == tuple:
                    desc, func = option
                else:
                    desc, func = None, None

                menu_option = (desc, func)
                if not desc and not func:
                    continue
                else:
                    menu_options.append(menu_option)
            except:
                continue

        for i, option in enumerate(menu_options):
            print(f"{i + 1}. {option[0]}")
        print("0. Exit")

        if info_bottom:
            print()
            print(info_bottom() if callable(info_bottom) else info_bottom)
        print()

        choice = input("Select an option: ").strip()

        if choice in ['0', 'q']:
            return
        elif choice.isdigit() and 0 <= int(choice) - 1 < len(menu_options):
            func_tmp = menu_options[int(choice) - 1][1]
            if type(func_tmp) == types.FunctionType:
                clear_screen()
                func_tmp()
        else:
            print("Wrong option. Try again.")
        print()
        input("Press ENTER to continue...")


def func_to_tuple(func):
    """Convert function to menu tuple"""
    if type(func) == types.FunctionType:
        desc, func_out = func()
        return (desc, func_out)
    return None
