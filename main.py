"""PROJECT WMX"""
"""The Ultimate Learing"""


# from src.globals.keyreader import KeyEnum, get_key
from src.menu_screens import *
from src.config.class_config import get_config_manager
from src.database.class_connection_manager import get_connection_manager


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

if __name__ == "__main__":
    # def main():
    config_manager = get_config_manager()
    connection_manager = get_connection_manager()

    clear_screen()
    # starting data load
    config_manager.load_config()
    connection_manager.reconnect()

    while True:
        """Main program loop"""
        main_menu()
        break


# start program
# main()
