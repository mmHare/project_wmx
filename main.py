"""PROJECT WMX"""
"""The Ultimate Learing"""


from src.users import UserService, UsersMenu
from src.menu_screens import *
from src.config import SettingsService
from src.database import DatabaseService


class MainMenu(MenuScreen):
    def __init__(self):
        super().__init__("Main menu", info_top=self.info_user_connection)

    def __del__(self):
        print("See Ya!")

    def info_user_connection(self):
        return DatabaseService.connected_db_str() + "\n" + UserService.get_logged_user_info()

    def prepare_list(self):
        result_list = []
        if not DatabaseService.is_connected:
            result_list.append(MenuOption(
                "Connect", DatabaseService.connect))
        if DatabaseService.is_connected and not UserService.is_logged:
            result_list.append(MenuOption(
                "Log in", UsersMenu.user_log_in))

        result_list.append(MenuOption(
            "Configuration settings", self.config_menu))
        result_list.append(MenuOption("Database settings",
                           self.db_settings_menu, "db"))
        result_list.append(MenuOption("User settings",
                                      self.user_menu, "usr"))

        if DatabaseService.is_connected and UserService.is_logged:
            result_list.append(MenuOption(
                "Dictionary tables", self.dict_tables_menu))
            result_list.append(MenuOption("Minigames", menu_minigames_select))
            result_list.append(MenuOption(
                "Math problems", self.math_problems_menu))
            result_list.append(MenuOption(
                "Log out", UsersMenu.user_log_out))
        result_list.append(MenuOption("About", about_screen))

        return result_list

    def config_menu(self):
        ConfigMenu().show_menu()

    def db_settings_menu(self):
        DbSettingsMenu().show_menu()

    def user_menu(self):
        UsersMenu().show_menu()

    def dict_tables_menu(self):
        DictTablesMenu().show_menu()

    def math_problems_menu(self):
        MathProblemsMenu().show_menu()


############# MAIN #############
if __name__ == "__main__":
    clear_screen()
    SettingsService.load_config()
    DatabaseService.reconnect()

    while True:
        """Main program loop"""
        MainMenu().show_menu()
        break
