"""PROJECT WMX"""
"""The Ultimate Learing"""


from src.database.class_connection_manager import get_connection_manager
from src.config.class_config import get_config_manager
from src.menu_screens import *


def main():
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
main()
