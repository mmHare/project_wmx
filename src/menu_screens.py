"""List of program menu screens"""

from src.config import *
from src.database import *
from src.users import *
from src.help_functions import *
from src.menu_functions import show_menu


def main_menu():
    """Main menu of the program"""

    options = [
        (lambda: menu_user_log if not user_manager.is_logged else None),
        ("Configuration settings", config_menu),
        ("Database settings", db_settings_screen),
        ("User settings", user_management_screen)
    ]

    show_menu("Main menu", options, info_top=get_logged_user_info)
    print("See Ya!")

########################################################


def config_menu():
    """Method to display configuration settings."""
    options = [
        ("View current settings", print_config),
        ("Change settings", change_settings),
        ("Restore to defaults", restore_settings)
    ]

    show_menu("Configuration settings", options)


def db_settings_screen():
    """Method to display database settings."""
    options = [
        ("Check database connection", check_db_connection),
        ("Reconnect to database", db_reconnect),
        # ("Change database type", change_db_type),
        ("Check database version", check_db_version)
    ]

    show_menu("Database settings", options)


def user_management_screen():
    """Method to display user settings."""

    options = [
        (menu_user_log),
        ("Register IP", menu_register_user),
        ("User list", menu_list_users),
        ("Add new user", menu_new_user),
        ("Delete user", menu_delete_user)
    ]

    show_menu("User settings", options)
