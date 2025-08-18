"""Menu showing the available options."""

import types

from src.globals.help_functions import clear_screen


def func_to_tuple(func):
    """Convert function to menu tuple"""
    if type(func) == types.FunctionType:
        desc, func_out = func()
        return (desc, func_out)
    return None


def parse_option(opt):
    try:
        if type(opt) == types.FunctionType:
            desc, func = opt()
        elif type(opt) == tuple:
            desc, func = opt
        else:
            desc, func = None, None
        return desc, func
    except:
        return None, None


def show_menu(title, options: list, info_top=None, info_bottom=None, conditional_options=None):
    """Display a menu with the given title and options.

    Args:
        title (str): The title of the menu.
        options (list): A list of tuples containing option descriptions and their corresponding functions. Or function returning such tuple.
        info_top (optional): Additional information to display at the top of the menu (str or func returning str). Defaults to None.
        info_bottom (optional): Additional information to display at the bottom of the menu (str or func returning str). Defaults to None.
        conditional_options (optional): A function that returns a list of additional menu options based on certain conditions. Defaults to None.
    """

    if len(options) == 0:
        return

    while True:
        clear_screen()
        menu_options = []
        print("=" * 10, title.upper(), "=" * 10)

        # header
        if info_top:
            print(info_top() if callable(info_top) else info_top)
            print()

        # options
        for option in options:
            desc, func = parse_option(option)
            if desc or func:
                menu_options.append((desc, func))

        # conditional options
        if conditional_options:
            for option in conditional_options():
                desc, func = parse_option(option)
                if desc or func:
                    menu_options.append((desc, func))

        # printing options
        for i, option in enumerate(menu_options):
            print(f"{i + 1}. {option[0]}")
        print("0. Exit")

        # footer
        if info_bottom:
            print()
            print(info_bottom() if callable(info_bottom) else info_bottom)
        print()

        # user input
        choice = input("Select an option: ").strip()

        if choice in ['0', 'q']:
            return
        elif choice.isdigit() and 0 <= int(choice) - 1 < len(menu_options):
            func_tmp = menu_options[int(choice) - 1][1]
            if type(func_tmp) == types.FunctionType:
                clear_screen()
                func_tmp()
        elif choice == "":
            continue
        else:
            print("Wrong option. Try again.")
        print()
        input("Press ENTER to continue...")
