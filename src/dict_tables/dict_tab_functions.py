from . import dictionary_table_manager


def list_dictionary_tables():
    table_list = [table for table in dictionary_table_manager.get_table_list()]
    for table in table_list:
        pass
    return
