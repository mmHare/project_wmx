"""List of program menu screens"""

from src.config import *
from src.database import *
from src.users import *
from src.help_functions import *
from src.menu_functions import show_menu
from src.minigames import *


def main_menu():
    """Main menu of the program"""

    options = [
        (menu_user_log_in_if_visible),
        (menu_connect),
        ("Configuration settings", config_menu),
        ("Database settings", db_settings_screen),
        ("User settings", user_management_screen),
        (get_menu_minigames),
        (menu_user_log_out_if_visible)
    ]

    show_menu("Main menu", options, info_top=info_user_connection)
    print("See Ya!")

########################################################


def info_user_connection():
    return connected_db_str() + "\n" + get_logged_user_info()

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
        ("Check database version", check_db_version),
        ("Change database type", change_db_type)
    ]

    show_menu("Database settings", options, info_top=connected_db_str)


def user_management_screen():
    """Method to display user settings."""

    options = [
        (menu_user_log_in_if_visible),
        (menu_register_user),
        ("User list", menu_list_users),
        ("Add new user", menu_new_user),
        (menu_delete_user_if_visible),
        (menu_user_log_out_if_visible)
    ]

    show_menu("User settings", options, info_top=get_logged_user_info)
