"""PROJECT WMX"""
"""The Ultimate Learing"""


from src.menu_screens import *
from src.globals import *
from src.config import config_manager
from src.database import connection_manager


def main():
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
