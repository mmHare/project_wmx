"""List of program menu screens"""

from src.config import *
from src.database import *
from src.users import *
from src.globals.help_functions import *
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
        (get_menu_minigames)
    ]

    show_menu("Main menu", options, info_top=info_user_connection,
              conditional_options=main_options_for_logged_user)
    print("See Ya!")

########################################################


def info_user_connection():
    return connected_db_str() + "\n" + get_logged_user_info()


def main_options_for_logged_user():
    # conditional options for main menu
    options_list = []
    if connection_manager.connection and user_manager.is_logged:
        # options_list.append(("Dictionary tables", dictionary_tables_screen))
        options_list.append(("Log out", menu_user_log_out))

    options_list.append(("About", about_screen))
    return options_list


########################################################

def about_screen():
    print("About this program:")
    print("PROJECT WMX - The Ultimate Learning Experience")
    print(f"Version {PROGRAM_VERSION}")
    print("Developed by: Wojciech & Maciej Zając")
    print("Description: This program is designed to help designers to gain Python exp")
    input("Press Enter to return to the main menu.")


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
        (menu_register_user),
        ("User list", menu_list_users),
        ("Add new user", menu_new_user),
    ]

    if connection_manager.connection and not user_manager.is_logged:
        options.insert(0, ("Log in", menu_user_log_in))
    elif connection_manager.connection and user_manager.is_logged:
        if user_manager.logged_user.is_admin:
            options.append(("Delete user", menu_delete_user))
        options.append(("Log out", menu_user_log_out))

    show_menu("User settings", options, info_top=get_logged_user_info)


def dictionary_tables_screen():
    """Method to display dictionary tables."""
    options = [
        # ("View all tables", view_all_tables),
        # ("Add new table", add_new_table),
        # ("Delete table", delete_table)
    ]

    show_menu("Dictionary tables", options)
