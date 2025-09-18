"""Menu UI after selecting dict table"""

from tkinter import Tk, filedialog
import csv
import os

from src.dict_tables.class_dict_table_manager import *
from src.class_menu import MenuOption, MenuScreen
from src.config.config_manager import get_config_manager


dict_tab_manager = get_dict_tab_manager()
config_manager = get_config_manager()


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

    def menu_export_table():
        nonlocal table
        table = dict_tab_manager.load_table(table_name)
        export_table(table)

    print(f"== {table.table_name.upper()} ==")
    options = [
        MenuOption("Details", show_tab_details),
        MenuOption("List items", show_tab_list_items),
        MenuOption("Add new item", show_tab_add_item),
        MenuOption("Delete item", show_delete_item),
        MenuOption("Export to CSV", menu_export_table)
    ]

    MenuScreen("Dictionary tables", options).show_menu()


def table_details(table: DictionaryTable):
    print(f"Table: {table.table_name}")
    print(f"Description: {table.description}")
    print(f"Access: {table.visibility}")
    if table.owner_id == UserService.logged_user:
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

    print(f"{table.table_name.upper()}:")
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


def export_table(table: DictionaryTable):
    print("-- Export table to CSV --")
    print("Please select path to save the file:")

    try:
        if config_manager.is_use_dialogs:
            # using dialog
            root = Tk()
            root.withdraw()  # hide main window
            root.update()
            root.attributes("-topmost", True)  # Force on top
            root.focus_force()

            export_dir = filedialog.asksaveasfilename(
                parent=root,
                initialfile=table.table_name,
                title="Save file as...",
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
            root.destroy()
        else:
            # console input
            export_dir = input()
            if not os.path.isdir(export_dir):
                if input("Directory does not exist. Do you want to create it? (y/n)\n") == 'y':
                    os.makedirs(export_dir)
                else:
                    return

        if export_dir:
            with open(export_dir, "w", newline='') as csvfile:
                table_writer = csv.writer(
                    csvfile, delimiter=config_manager.get_csv_delim)
                table_writer.writerow(table.columns)
                table_writer.writerows([[value for value in item.values()]
                                        for item in table.items])
            print("Table exported successfully.")
        else:
            print("No path selected.")
    except Exception as e:
        print("Error while exporting to file:", e)
