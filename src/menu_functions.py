"""Menu showing the available options."""

import types

from src.globals.help_functions import clear_screen


class MenuScreen:
    def __init__(self, title, options: list, info_top=None, info_bottom=None):
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
    def title(self):
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
    def options(self):
        return self.__options

    @options.setter
    def options(self, value):
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

    def parse_option(self, opt):
        try:
            if type(opt) == types.FunctionType:
                desc, func, command = (opt() + (None,) * 3)[:3]
            elif type(opt) == tuple:
                desc, func, command = (opt + (None,) * 3)[:3]
            else:
                desc, func, command = None, None, None
            return desc, func, command
        except:
            return None, None, None

    def show_menu(self, conditional_options=None):
        """Display a menu with the given title and options.
            Options tuple (description, function, command) - if description is None function will not be printed on the menu;
            if command str is provided, then entering '/' and command, the function will be called (even if not visible)

        Args:
            title (str): The title of the menu.
            options (list): A list of tuples containing option descriptions and their corresponding functions. Or function returning such tuple.
            info_top (optional): Additional information to display at the top of the menu (str or func returning str). Defaults to None.
            info_bottom (optional): Additional information to display at the bottom of the menu (str or func returning str). Defaults to None.
            conditional_options (optional): A function that returns a list of additional menu options based on certain conditions. Defaults to None.
        """

        if len(self.options) == 0:
            return

        while True:
            clear_screen()
            menu_options = []
            print("=" * 10, self.title.upper(), "=" * 10)

            # header
            self.print_info_top()

            # options
            for option in self.options:
                desc, func, command = self.parse_option(option)
                if desc or func:
                    menu_options.append((desc, func, command))

            # conditional options
            if conditional_options:
                for option in conditional_options():
                    desc, func, command = self.parse_option(option)
                    if desc or func:
                        menu_options.append((desc, func, command))

            # printing options
            visible_options = [
                opt for opt in menu_options if opt[0] is not None]
            for i, option in enumerate(visible_options):
                print(f"{i + 1}. {option[0]}")
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
                # command = command[1:]
                for option in menu_options:
                    func_tmp = option[1]
                    if (option[2] == command) and (type(func_tmp) == types.FunctionType):
                        clear_screen()
                        func_tmp()
                        break
            elif choice.isdigit() and 0 <= int(choice) - 1 < len(visible_options):
                # selected from printed options
                func_tmp = visible_options[int(choice) - 1][1]
                if type(func_tmp) == types.FunctionType:
                    clear_screen()
                    func_tmp()
            elif choice == "":
                continue
            else:
                print("Wrong option. Try again.")
            print()
            input("Press ENTER to continue...")
