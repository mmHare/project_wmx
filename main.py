"""PROJECT WMX"""
"""The Ultimate Learing"""


# from src.globals.keyreader import KeyEnum, get_key
from src.config.class_config import get_config_manager
from src.database.class_connection_manager import get_connection_manager
from src.menu_screens import *


# print("Before get key")


# if key == KeyEnum.KEY_Q:
#     print("Quit pressed")
#     # break
# elif key != KeyEnum.KEY_UNKNOWN:
#     print("Special key pressed:", key)
# else:
# key = get_key()
# if key == KeyEnum.KEY_UP:
#     print("up up")
# else:
#     user_input = input("Enter text: ")
#     print("You typed:", user_input)


# key = get_key()
# if key == KeyEnum.KEY_A:
#     print("it was a")
# else:
#     usrin = input()
#     print(usrin)

# print("after get key")
# input()

class MainMenu(MenuScreen):
    def __init__(self):
        self.options = []
        self.options.append(MenuOption.from_func(menu_user_log_in_if_visible))
        self.options.append(MenuOption.from_func(menu_connect))
        self.options.append(MenuOption("Configuration settings", config_menu))
        self.options.append(MenuOption(
            "Database settings", db_settings_screen, "db"))
        self.options.append(MenuOption("User settings",
                                       user_management_screen, "usr"))

        super().__init__("Main menu", self.options, info_top=self.info_user_connection)

    def __del__(self):
        print("See Ya!")

    def info_user_connection(self):
        return connected_db_str() + "\n" + get_logged_user_info()

    def main_options_for_logged_user(self):
        # conditional options for main menu
        options_list = []
        if connection_manager.connection and user_manager.is_logged:
            # options available when user is logged in
            options_list.append(MenuOption(
                "Dictionary tables", dictionary_tables_screen))
            options_list.append(MenuOption("Minigames", menu_minigames_select))
            options_list.append(MenuOption(
                "Math problems", math_problems_screen))
            options_list.append(MenuOption("Log out", menu_user_log_out))

        options_list.append(MenuOption("About", about_screen))
        return options_list

    def show_menu(self):
        return super().show_menu(self.main_options_for_logged_user)


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
