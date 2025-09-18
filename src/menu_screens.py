"""List of program menu screens"""

from src.globals.help_functions import *
from src.class_menu import MenuScreen, MenuOption
from src.config import SettingsService
from src.database import DatabaseService
from src.dict_tables.menu_dict_tab import *
from src.minigames import *
from src.users.user_service import UserService


class ConfigMenu(MenuScreen):
    def __init__(self):
        super().__init__("Configuration settings")
        self.options = [
            MenuOption("View current settings", SettingsService.print_config),
            MenuOption("Change settings", self.settings_changed),
            MenuOption("Restore to defaults", SettingsService.restore_settings)
        ]

    def settings_changed(self):
        if SettingsService.change_settings():
            UserService.log_out()
            DatabaseService.reconnect()


class DbSettingsMenu(MenuScreen):
    def __init__(self):
        super().__init__("Database settings", info_top=DatabaseService.connected_db_str)
        self.options = [
            MenuOption("Check database connection",
                       DatabaseService.check_db_connection),
            MenuOption("Reconnect to database", DatabaseService.reconnect),
            MenuOption("Check database version",
                       DatabaseService.check_db_version),
            MenuOption("Change database type", self.settings_changed)
        ]

    def settings_changed(self):
        if DatabaseService.change_db_type():
            UserService.log_out()
            DatabaseService.reconnect()


class DictTablesMenu(MenuScreen):
    def __init__(self):
        super().__init__("Dictionary tables")

        self.options = [
            MenuOption("List tables", menu_list_tables),
            MenuOption("Add new table", menu_new_table),
            MenuOption("Delete table", menu_delete_table),
            MenuOption("Select table", menu_select_table),
            MenuOption("Import table", menu_import_table)
        ]


class MathProblemsMenu(MenuScreen):
    def __init__(self):
        super().__init__("Math problems")

        self.options = []


def about_screen():
    print("About this program:")
    print("PROJECT WMX - The Ultimate Learning Experience")
    print(f"Version {PROGRAM_VERSION}")
    print("Developed by: Wojciech & Maciej Zając")
    print("This program is designed to help designers gain Python exp")
