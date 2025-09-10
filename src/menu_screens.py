"""List of program menu screens"""

from src.globals.help_functions import *
from src.class_menu import MenuScreen, MenuOption
from src.config.config_functions import *
from src.database.db_functions import *
from src.users.users_functions import *
from src.dict_tables.dict_tab_functions import *
from src.minigames import *


class UserMenu(MenuScreen):
    def __init__(self):
        super().__init__("User settings", [])

    def prepare_list(self):
        result_list = []
        if connection_manager.connection and not user_manager.is_logged:
            result_list.append(MenuOption("Log in", menu_user_log_in))

        result_list.append(MenuOption("User list", menu_list_users))
        result_list.append(MenuOption("Add new user", menu_new_user))

        if connection_manager.connection and user_manager.is_logged:
            if user_manager.logged_user.is_admin:
                result_list.append(MenuOption("Delete user", menu_delete_user))
            result_list.append(MenuOption(
                "Conversation", menu_user_conversation))
            result_list.append(MenuOption.from_func(menu_register_user))
            result_list.append(MenuOption("Log out", menu_user_log_out))

        self.info_top = get_logged_user_info()
        return result_list


def about_screen():
    print("About this program:")
    print("PROJECT WMX - The Ultimate Learning Experience")
    print(f"Version {PROGRAM_VERSION}")
    print("Developed by: Wojciech & Maciej Zając")
    print("This program is designed to help designers gain Python exp")
    input("Press Enter to return to the main menu.")


def config_menu():
    """Method to display configuration settings."""
    def settings_changed():
        if change_settings():
            user_manager.log_out()
            connection_manager.reconnect()

    options = [
        MenuOption("View current settings", print_config),
        MenuOption("Change settings", settings_changed),
        MenuOption("Restore to defaults", restore_settings)
    ]

    MenuScreen("Configuration settings", options).show_menu()


def db_settings_screen():
    """Method to display database settings."""
    def settings_changed():
        if change_db_type():
            user_manager.log_out()
            connection_manager.reconnect()

    options = [
        MenuOption("Check database connection", check_db_connection),
        MenuOption("Reconnect to database", db_reconnect),
        MenuOption("Check database version", check_db_version),
        MenuOption("Change database type", settings_changed)
    ]

    MenuScreen("Database settings", options,
               info_top=connected_db_str).show_menu()


def dictionary_tables_screen():
    """Method to display dictionary tables options"""
    options = [
        MenuOption("List tables", menu_list_tables),
        MenuOption("Add new table", menu_new_table),
        MenuOption("Delete table", menu_delete_table),
        MenuOption("Select table", menu_select_table),
        MenuOption("Import table", menu_import_table)
    ]

    MenuScreen("Dictionary tables", options).show_menu()


def math_problems_screen():
    """Method displaying screen of Math Problems screen"""
    options = []

    MenuScreen("Math problems", options).show_menu()
