"""List of program menu screens"""

import types
from src.config import *
from src.database import *
from src.users import *
from src.help_functions import *


def show_menu(title, options: list):
    """Printing menu from given options - tuples (name, func)"""
    if len(options) == 0:
        return

    while True:
        clear_screen()
        print("=" * 10, title.upper(), "=" * 10)
        for i, option in enumerate(options):
            print(f"{i + 1}. {option[0]}")
        print("0. Exit")

        choice = input("Select an option: ").strip()

        if choice in ['0', 'q']:
            return
        elif choice.isdigit() and 0 <= int(choice) - 1 < len(options):
            func_tmp = options[int(choice) - 1][1]
            if type(func_tmp) == types.FunctionType:
                clear_screen()
                func_tmp()
        else:
            print("Wrong option. Try again.")
        print()
        input("Press ENTER to continue...")


def display_menu(functions_list: list):
    print()
    print("="*10, "MENU", "="*10)
    print("0 - Exit")
    for function in functions_list:
        command = functions_list.index(function) + 1
        name = function.__name__.replace("_", " ").title()
        print(f"{command} - {name}")


########################################################

# Configuration
def config_menu():
    """Method to display configuration settings."""
    options = [
        ("View current settings", print_config),
        ("Change settings", change_settings),
        ("Restore to defaults", restore_settings)
    ]

    show_menu("Configuration settings", options)


# Database
def db_settings_screen():
    """Method to display database settings."""
    options = [
        ("Check database connection", check_db_connection),
        ("Reconnect to database", db_reconnect),
        # ("Change database type", change_db_type),
        ("Check database version", check_db_version)
    ]

    show_menu("Database settings", options)


# Users
def user_management_screen():
    """Method to display user settings."""

    options = [
        ("Log out" if user_manager.is_logged else "Log in", menu_user_log_in_log_out),
        ("Register IP", menu_register_user),
        ("User list", menu_list_users),
        ("Add new user", menu_new_user),
        ("Delete user", menu_delete_user)
    ]

    show_menu("User settings", options)


############################################################


def main_menu():
    """Main menu of the program"""

    options = [
        ("Configuration settings", config_menu),
        ("Database settings", db_settings_screen),
        ("User settings", user_management_screen)
    ]

    show_menu("Main menu", options)
    print("See Ya!")
