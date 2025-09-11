"""PROJECT WMX"""
"""The Ultimate Learing"""


from src.menu_screens import *
from src.config.class_config import get_config_manager
from src.database.class_connection_manager import get_connection_manager


class MainMenu(MenuScreen):
    def __init__(self):
        super().__init__("Main menu", info_top=self.info_user_connection)

    def __del__(self):
        print("See Ya!")

    def info_user_connection(self):
        return connected_db_str() + "\n" + get_logged_user_info()

    def prepare_list(self):
        result_list = []
        if not connection_manager.connection:
            result_list.append(MenuOption("Connect", db_connect))
        if connection_manager.connection and not user_manager.is_logged:
            result_list.append(MenuOption("Log in", menu_user_log_in))

        result_list.append(MenuOption(
            "Configuration settings", self.config_menu))
        result_list.append(MenuOption("Database settings",
                           self.db_settings_menu, "db"))
        result_list.append(MenuOption("User settings",
                                      self.user_menu, "usr"))

        if connection_manager.connection and user_manager.is_logged:
            result_list.append(MenuOption(
                "Dictionary tables", self.dict_tables_menu))
            result_list.append(MenuOption("Minigames", menu_minigames_select))
            result_list.append(MenuOption(
                "Math problems", self.math_problems_menu))
            result_list.append(MenuOption("Log out", menu_user_log_out))
        result_list.append(MenuOption("About", about_screen))

        return result_list

    def config_menu(self):
        ConfigMenu().show_menu()

    def db_settings_menu(self):
        DbSettingsMenu().show_menu()

    def user_menu(self):
        UserMenu().show_menu()

    def dict_tables_menu(self):
        DictTablesMenu().show_menu()

    def math_problems_menu(self):
        MathProblemsMenu().show_menu()


############# MAIN #############
if __name__ == "__main__":
    config_manager = get_config_manager()
    connection_manager = get_connection_manager()

    clear_screen()
    config_manager.load_config()
    connection_manager.reconnect()

    while True:
        """Main program loop"""
        MainMenu().show_menu()
        break
