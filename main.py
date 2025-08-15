"""PROJECT WMX"""
"""The Ultimate Learing"""


from src.config import config_manager
from src.database import connection_manager
from src.globals import *
from src.menu_screens import *


# starting data load


def main():
    clear_screen()
    config_manager.load_config()
    connection_manager.reconnect()

    while True:
        """Main program loop"""
        main_menu()
        break


main()
