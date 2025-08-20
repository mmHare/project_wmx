"""Functions regarding dictionary tables"""

from src.globals.help_functions import clear_screen
from .class_dict_table_manager import *
from src.users.class_user_manager import get_user_manager
from .dict_tab_options import table_options

dict_tab_manager = get_dict_tab_manager()
user_manager = get_user_manager()


def print_table(table: DictionaryTable):
    if not table:
        return
    print("-"*20)
    print("Table:", table.table_name.capitalize())
    print("Access:", table.visibility)
    if not table.description == "":
        print(table.description)
    print("Columns:")
    for i, col in enumerate(table.columns):
        print(f"{i + 1}. {col}")
    print("-"*20)


def list_dictionary_tables(table_list: list[DictionaryTable] = None):
    if not table_list:
        table_list = dict_tab_manager.get_table_list()
    i = 1
    usr_id = user_manager.logged_user.id
    for table in table_list:
        if (table.is_public) or (table.owner_id == usr_id):
            print(f"{i}. {table.table_name}")
            i += 1
    return


def menu_list_tables():
    def filter_tables(tab: DictionaryTable):
        return tab.is_public or tab.owner_id == user_manager.logged_user.id

    table_list = dict_tab_manager.get_table_list()

    if not table_list:
        print("No tables to show.")
    else:
        tables_to_show = list(filter(filter_tables, table_list))

        if len(tables_to_show) == 0:
            print("No tables to show.")
        else:
            list_dictionary_tables(table_list)

    print()


def menu_new_table():
    tab_name = ""
    columns = []

    while True:
        clear_screen()
        print("-- New dictionary table --")
        user_input = input("Table name: ")
        if user_input == "":
            print(
                "Table name cannot be empty. Input 'q' to quit or press ENTER to continue.")
            if input() == 'q':
                return
        elif not all(ch.isalnum() or ch in ["_"] for ch in user_input):
            print("Only letters, digits and underscores are eligible.")
        elif (user_input[0].isdigit()) or (user_input[0] == "_"):
            print("Name must start with a letter.")
        elif len(user_input) > 25:
            print("Name cannot exceed 25 characters.")
        else:
            tab_name = user_input
            break
        input("Press ENTER to continue...")

    print()
    print("Enter column names. Leave empty when you're done and want to continue.")
    i = 1
    while True:
        user_input = input(f"{i}. ")
        if user_input == "":
            if not (0 < len(columns) < 5):
                print("Table needs to have 1-5 columns.")
            else:
                break
        elif not all(ch.isalnum() or ch in ["_"] for ch in user_input):
            print("Only letters, digits and underscores are eligible.")
        elif (user_input[0].isdigit()) or (user_input[0] == "_"):
            print("Name must start with a letter.")
        elif len(user_input) > 25:
            print("Name cannot exceed 25 characters.")
        else:
            columns.append(user_input)
            i += 1
            continue
        input("Press ENTER to continue...")

    table = DictionaryTable(tab_name, list(set(columns)))

    print()
    if input("Do you want to add description to the table? (y/n) ") == 'y':
        table.description = input("Description: ")

    print()
    while True:
        user_input = input(
            "Do you want this table to be 'private' or 'public' (visible to other users)?\n").lower()
        if user_input not in ['private', 'public']:
            print("Please enter 'private' or 'public'")
        else:
            table.visibility = user_input
            break

    clear_screen()
    print("Summary")
    print_table(table)
    if input("Do you want to create this table? ('y' to confirm)\n") == "y":
        dict_tab_manager.create_table(table)


def menu_delete_table():
    clear_screen()
    print("-- Delete table --")

    while True:
        user_input = input("Name of the table to delete:\n")
        if user_input == "":
            print(
                "Table name cannot be empty. Input 'q' to quit or press ENTER to continue.")
            if input() == 'q':
                return
        elif not all(ch.isalnum() or ch in ["_"] for ch in user_input):
            print("Only letters, digits and underscores are eligible.")
            input("Press ENTER to continue...")
        elif (user_input[0].isdigit()) or (user_input[0] == "_"):
            print("Name must start with a letter.")
            input("Press ENTER to continue...")
        else:
            if input(f"Do you want to delete table {user_input}? ('y' to confirm)\n") == 'y':
                table = DictionaryTable(user_input)
                if dict_tab_manager.delete_table(table):
                    print("Table deleted successfully.")
            return


def menu_select_table():
    clear_screen()
    print("-- Select table --")

    while True:
        print("Enter name of the table to show its options. (0 to quit)")
        user_input = input().strip()
        if user_input == "":
            continue
        elif user_input == '0':
            break
        elif not all(ch.isalnum() or ch in ["_"] for ch in user_input) or (user_input[0].isdigit()) or (user_input[0] == "_"):
            print("Invalid name.")
        elif not dict_tab_manager.check_table_status(DictionaryTable(user_input)) == TableCheckResult.USABLE:
            print("This table is not available.")
        else:
            table_options(user_input)
            return
