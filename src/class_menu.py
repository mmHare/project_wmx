"""Menu showing the available options."""

import types
from typing import Callable, Optional, Tuple
from src.globals.help_functions import clear_screen


class MenuOption:
    def __init__(self, description: str, function: types.FunctionType, command: Optional[str] = None):
        """
        Args:
            description (str): String being shown in the menu
            function (types.FunctionType): Function assigned to the option
            command (Optional[str], optional): Command str assigned to use instead of number. Defaults to None.
        """
        self.description = description
        self.func = function
        self.command = command

    @classmethod
    def from_func(cls, tuple_function: Callable[[], Tuple[str, types.FunctionType]], command: Optional[str] = None):
        description, function = tuple_function()
        return cls(description, function, command)

    def __call__(self):
        if callable(self.func):
            self.func()


########### MENU SCREEN ###########

class MenuScreen:
    def __init__(self, title, options: list[MenuOption] = [], info_top=None, info_bottom=None):
        self.__title = None
        self.__options = None
        self.__info_top = None
        self.__info_bottom = None

        self.title = title
        self.info_top = info_top
        self.info_bottom = info_bottom
        self.options = options


########### PROPERTIES ###########

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def info_top(self):
        return self.__info_top

    @info_top.setter
    def info_top(self, value):
        self.__info_top = value

    @property
    def info_bottom(self):
        return self.__info_bottom

    @info_bottom.setter
    def info_bottom(self, value):
        self.__info_bottom = value

    @property
    def options(self) -> list[MenuOption]:
        return self.__options

    @options.setter
    def options(self, value: list[MenuOption]):
        if not value:
            self.__options = []
        else:
            for v in value:
                if not isinstance(v, MenuOption):
                    raise ValueError(
                        "Options list should contain only MenuOption objects.")
            self.__options = value

########### METHODS ###########

    def print_info_top(self):
        if self.info_top:
            print(self.info_top() if callable(
                self.info_top) else self.info_top)
            print()

    def print_info_bottom(self):
        if self.info_bottom:
            print()
            print(self.info_bottom() if callable(
                self.info_bottom) else self.info_bottom)

    def func_to_tuple(self, func):
        """Convert function to menu tuple"""
        if type(func) == types.FunctionType:
            desc, func_out = func()
            return (desc, func_out)
        return None

    def prepare_list(self) -> list[MenuOption]:
        """Option for dynamic (refreshing with each iteration) adjusting list, result list which will be shown on the screen."""
        return self.options

    def show_menu(self):
        """Display menu options screen."""

        while True:
            screen_options = self.prepare_list()
            if len(screen_options) == 0:
                print("No available options.\n")
                input("Press ENTER to continue...")
                return

            clear_screen()
            menu_options = []
            print("=" * 10, self.title.upper(), "=" * 10)

            # header
            self.print_info_top()

            # options
            for option in screen_options:
                if option.description or option.func:
                    menu_options.append(option)

            # printing options
            visible_options = [
                opt for opt in menu_options if opt.description is not None]
            for i, option in enumerate(visible_options):
                print(f"{i + 1}. {option.description}")
            print("0. Exit")

            # footer
            self.print_info_bottom()
            print()

            # user input
            choice = input("Select an option: ").strip()

            if choice in ['0', 'q']:
                return
            elif choice.startswith("/"):
                # searching through commands
                command = choice.split()[0][1:]
                for option in menu_options:
                    if (option.command == command):
                        clear_screen()
                        option()
                        break
            elif choice.isdigit() and 0 <= int(choice) - 1 < len(visible_options):
                # selected from printed options
                option = visible_options[int(choice) - 1]
                clear_screen()
                option()
            elif choice == "":
                continue
            else:
                print("Wrong option. Try again.")
            print()
            input("Press ENTER to continue...")
