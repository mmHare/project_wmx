"""Functions regarding dictionary tables"""

from src.globals.help_functions import clear_screen
from src.globals.glob_constants import *
from .class_dictionary_table import *
from src.users.class_user_manager import get_user_manager

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
        if (table.is_public) or (table.created_by == usr_id):
            print(f"{i}. {table.table_name}")
            i += 1
    return


def menu_list_tables():
    table_list = dict_tab_manager.get_table_list()

    usr_id = user_manager.logged_user.id
    tables_to_show = [table for table in table_list if (
        table.is_public) or (table.created_by == usr_id)]

    # ^- zamiast tego, wyciągnąć tabele filtrem

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
        elif not all(ch.isalpha() or ch in ["_"] for ch in user_input):
            print("Only letters and underscores are eligible.")
        elif user_input[0] == "_":
            print("Name cannot start with underscore.")
        else:
            tab_name = user_input
            break

    print()
    print("Enter column names. Leave empty when you're done and want to continue.")
    i = 1
    while True:
        user_input = input(f"{i}. ")
        if user_input == "":
            break
        elif not all(ch.isalpha() or ch in ["_"] for ch in user_input):
            print("Only letters and underscores are eligible.")
        elif user_input[0] == "_":
            print("Name cannot start with underscore.")
        else:
            columns.append(user_input)
            i += 1

    table = DictionaryTable(tab_name, list(set(columns)))

    print()
    if input("Do you want to add description to the table? (y/n) "):
        table.description = input("Description: ")

    print()
    while True:
        user_input = input(
            "Do you want this table to be 'private' or 'public' (visible to other users)?\n")
        if user_input not in [ACC_PRIVATE, ACC_PUBLIC]:
            print(F"Please enter {ACC_PRIVATE} or {ACC_PUBLIC}")
        else:
            table.visibility = user_input
            break

    clear_screen()
    print("Summary")
    print_table(table)
    if input("Do you want to create this table? ('y' to confirm)\n") == "y":
        dict_tab_manager.create_table(table)


def menu_delete_table():
    pass
