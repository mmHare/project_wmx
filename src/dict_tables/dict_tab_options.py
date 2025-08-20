"""Menu UI regarding Dict Table"""


from functools import partial
from src.dict_tables.class_dict_table_manager import *
from src.menu_functions import show_menu

dict_tab_manager = get_dict_tab_manager()


def table_options(table: DictionaryTable):
    dict_tab_manager.load_table(table)
    if not table:
        print("No data to show.")
        return

    menu_tab_details = partial(table_details, table)
    menu_tab_list_items = partial(table_list_items, table)
    menu_tab_add_item = partial(table_add_item, table)
    menu_tab_delete_item = partial(table_delete_item, table)

    print(f"== {table.table_name.upper()} ==")
    options = [
        ("Details", menu_tab_details),
        ("List items", menu_tab_list_items),
        ("Add new item", menu_tab_add_item),
        ("Delete item", menu_tab_delete_item)
    ]

    show_menu("Dictionary tables", options)


def table_details(table: DictionaryTable):
    clear_screen()
    print(f"Table: {table.table_name}")
    print()


def table_list_items(table: DictionaryTable):
    pass


def table_add_item(table: DictionaryTable):
    pass


def table_delete_item(table: DictionaryTable):
    pass
