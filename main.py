"""PROJECT WMX"""
"""The Ultimate Learing"""


# from src.globals.keyreader import KeyEnum, get_key
from src.database.class_connection_manager import get_connection_manager
from src.menu_screens import *
from src.config.class_config import get_config_manager


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
        self.options.append(MenuOption.from_func(menu_connect))
        self.options.append(MenuOption("Configuration settings", config_menu))
        self.options.append(MenuOption(
            "Database settings", db_settings_screen, "db"))
        self.options.append(MenuOption("User settings",
                                       self.user_menu, "usr"))

        super().__init__("Main menu", self.options, info_top=self.info_user_connection)

    def __del__(self):
        print("See Ya!")

    def info_user_connection(self):
        return connected_db_str() + "\n" + get_logged_user_info()

    def prepare_list(self):
        result_list = []
        if connection_manager.connection and not user_manager.is_logged:
            result_list.append(MenuOption("Log in", menu_user_log_in))

        result_list += self.options

        if connection_manager.connection and user_manager.is_logged:
            result_list.append(MenuOption(
                "Dictionary tables", dictionary_tables_screen))
            result_list.append(MenuOption("Minigames", menu_minigames_select))
            result_list.append(MenuOption(
                "Math problems", math_problems_screen))
            result_list.append(MenuOption("Log out", menu_user_log_out))
        result_list.append(MenuOption("About", about_screen))

        return result_list

    def user_menu(self):
        UserMenu().show_menu()

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
