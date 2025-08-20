"""Menu UI regarding Dict Table"""


from functools import partial
from src.dict_tables.class_dict_table_manager import *
from src.menu_functions import show_menu

dict_tab_manager = get_dict_tab_manager()
user_manager = get_user_manager()


def table_options(table_name: str):
    table = dict_tab_manager.load_table(table_name)
    if not table:
        print("No data to show.")
        return

    def show_tab_details():
        nonlocal table
        table = dict_tab_manager.load_table(table_name)
        table_details(table)

    def show_tab_list_items():
        nonlocal table
        table = dict_tab_manager.load_table(table_name)
        table_list_items(table)

    def show_tab_add_item():
        nonlocal table
        table_add_item(table)
        table = dict_tab_manager.load_table(table_name)

    def show_delete_item():
        nonlocal table
        table_delete_item(table)
        table = dict_tab_manager.load_table(table_name)

    # while True:
    #     clear_screen()
    #     print("== DICTIONARY TABLES ==")
    #     print("1. Details")
    #     print("2. List items")
    #     print("3. Add new item")
    #     print("4. Delete item")
    #     print("0. Exit")
    #     user_input = input("Select option: ")

    #     if user_input == '0':
    #         break
    #     elif user_input not in ['1', '2', '3', '4']:
    #         print("Wrong option.")
    #     elif user_input == '1':
    #         table_details(table)
    #     elif user_input == '2':
    #         table_list_items(table)
    #     elif user_input == '3':
    #         table_add_item(table)
    #     elif user_input == '4':
    #         table_delete_item(table)

    # input("Press ENTER to continue...")

    print(f"== {table.table_name.upper()} ==")
    options = [
        ("Details", show_tab_details),
        ("List items", show_tab_list_items),
        ("Add new item", show_tab_add_item),
        ("Delete item", show_delete_item)
    ]

    show_menu("Dictionary tables", options)


def table_details(table: DictionaryTable):
    print(f"Table: {table.table_name}")
    print(f"Description: {table.description}")
    print(f"Access: {table.visibility}")
    if table.owner_id == user_manager.logged_user:
        print("You are the owner.")
    print("Columns:")
    for col in table.columns:
        print(f"  {col}")
    print(f"Number of items: {len(table.items)}")
    print()


def table_list_items(table: DictionaryTable):
    if len(table.items) == 0:
        print("No items to show.")
        return

    item_lines = []
    for item in table.items:
        item_line = ' | '.join([str(item[col]) for col in table.columns])
        item_lines.append(item_line)

    print(f"{table.table_name.upper()}: list of items")
    max_line = len(max(item_lines))
    print("_"*max_line)
    column_line = ' | '.join(table.columns)
    print(column_line)
    print("-"*max_line)
    for line in item_lines:
        print(line)
    print("-"*max_line)


def table_add_item(table: DictionaryTable):
    print("Add item:")
    item = dict()
    for col in table.columns:
        if col == "id":
            continue
        item[col] = input(f"{col}: ")

    if input(f"Do you really want to add this item to the table {table.table_name}? 'y' to confirm: ") == 'y':
        dict_tab_manager.add_item(table, item)


def table_delete_item(table: DictionaryTable):
    item_id = input("Enter id of an item to delete: ")
    if not item_id.isdigit():
        print("ID must be a number!")
    item_id = int(item_id)
    sel_item = [item for item in table.items if item["id"] == item_id]
    if len(sel_item) == 0:
        print(f"Error: Item with id = {item_id} not found.")
    elif len(sel_item) > 1:
        print(f"Error: Multiple items found.")
    else:
        dict_tab_manager.delete_item_by_id(table, item_id)
