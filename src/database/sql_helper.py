"""Reusable universal SQL query handlers for Postgre and SQLite"""

import re
import sqlite3
from typing import Optional
from psycopg2.extras import RealDictCursor

from src.globals.glob_enums import DbType, QueryMode


def prepare_sql_text(sql_text: str, params: dict, db_type: DbType) -> str:
    """
    Formats sql_text with parameters starting with ':' (e.g. ':par') for given DB type.
    For SQLite, leaves ':param' as-is.
    For Postgres, converts ':param' -> '%(param)s'.
    Returns the formatted SQL string.
    """
    if db_type not in (DbType.POSTGRES, DbType.SQLITE):
        raise ValueError("Database not supported")

    if db_type == DbType.POSTGRES:
        def replacer(match: re.Match) -> str:
            name = match.group(1)
            if name not in params:
                raise ValueError(f"Missing parameter: {name}")
            return f"%({name})s"
        sql_text = re.sub(r":(\w+)", replacer, sql_text)

    if not sql_text.endswith(";"):
        sql_text += ";"
    return sql_text


def query_select(connection, db_type: DbType, sql_text: str, params: Optional[dict] = None,
                 fetch_one: bool = False, dict_result: bool = False):
    """Executes a SELECT query and returns results."""
    if not connection:
        raise ValueError("No connection provided")

    if dict_result and db_type == DbType.SQLITE:
        connection.row_factory = sqlite3.Row

    if db_type == DbType.POSTGRES:
        cursor = connection.cursor(
            cursor_factory=RealDictCursor if dict_result else None)
    else:  # SQLite
        cursor = connection.cursor()

    if params:
        sql_text = prepare_sql_text(sql_text, params, db_type)
        cursor.execute(sql_text, params)
    else:
        cursor.execute(sql_text)

    rows = cursor.fetchone() if fetch_one else cursor.fetchall()

    if dict_result and db_type == DbType.SQLITE:
        if rows is None:
            return None
        if fetch_one:
            return dict(rows)
        return [dict(row) for row in rows]

    return rows


def query_modify(connection, db_type: DbType, mode: QueryMode, sql_text: str,
                 params: Optional[dict] = None, key_fields: Optional[tuple] = None):
    """
    Executes INSERT / UPDATE / DELETE / UPSERT queries.

    For UPSERT, key_fields must be provided as a tuple of unique columns.
    """
    if not connection:
        raise ValueError("No connection provided")

    start_text = sql_text.lstrip().upper()
    if (mode == QueryMode.UPSERT) and (start_text.startswith("INSERT INTO")):
        pass
    elif not start_text.startswith(mode.value.upper()):
        raise ValueError("Query statement and mode inconsistent")

    # Handle UPSERT
    if mode == QueryMode.UPSERT:
        if not key_fields:
            raise ValueError("key_fields must be provided for UPSERT")

        sql_text = sql_text.strip().rstrip(";")
        match = re.search(r"\((.*?)\)\s*VALUES", sql_text,
                          re.IGNORECASE | re.DOTALL)
        if not match:
            raise ValueError("Cannot parse column list from INSERT statement.")

        all_columns = [col.strip() for col in match.group(1).split(",")]
        update_columns = [col for col in all_columns if col not in key_fields]
        if not update_columns:
            raise ValueError("No columns to update (all are key fields).")

        if db_type == DbType.POSTGRES:
            upsert_suffix = (
                f" ON CONFLICT ({', '.join(key_fields)}) DO UPDATE SET "
                + ", ".join([f"{col} = EXCLUDED.{col}" for col in update_columns])
            )
            sql_text += upsert_suffix
        elif db_type == DbType.SQLITE:
            upsert_suffix = (
                f" ON CONFLICT ({', '.join(key_fields)}) DO UPDATE SET "
                + ", ".join([f"{col} = excluded.{col}" for col in update_columns])
            )
            sql_text += upsert_suffix

    cursor = connection.cursor()

    if params:
        sql_text = prepare_sql_text(sql_text, params, db_type)
        cursor.execute(sql_text, params)
    else:
        cursor.execute(sql_text)

    if mode in (QueryMode.INSERT, QueryMode.UPSERT):
        if db_type == DbType.POSTGRES:
            cursor.execute("SELECT LASTVAL();")
            new_id = cursor.fetchone()[0]
        elif db_type == DbType.SQLITE:
            new_id = cursor.lastrowid
        connection.commit()
        return new_id
    else:  # UPDATE / DELETE
        connection.commit()
        return cursor.rowcount


############### DEPRECATED - executing into positional format ###############

# def prepare_sql_text(sql_text: str, params: dict, db_type: DbType) -> tuple[str, tuple]:
#     """
#     Formats sql_text with parameters starting with ':' (e.g. ':par') for given DB type.
#     Parameters are matched against `params` dict of param_name -> value.
#     Returns formatted SQL text and tuple of values in order of occurrence.
#     """
#     if db_type not in (DbType.POSTGRES, DbType.SQLITE):
#         raise ValueError("Database not supported")

#     placeholder = "%s" if db_type == DbType.POSTGRES else "?"
#     values = []

#     def replacer(match: re.Match) -> str:
#         name = match.group(1)  # the part after ':'
#         if name not in params:
#             raise ValueError(f"Missing parameter: {name}")
#         values.append(params[name])
#         return placeholder

#     # regular to find parameters :param_name
#     sql_text = re.sub(r":(\w+)", replacer, sql_text)
#     return sql_text, tuple(values)


# def prepare_upsert_sql(db_type: DbType, insert_part: list, update_part: list, key_fields: list):
#     if insert_part is None or update_part is None or key_fields is None:
#         raise ValueError("Invalid arguments")

#     if not isinstance(insert_part[0], str) or not insert_part[0].lstrip().upper().startswith("INSERT INTO"):
#         raise ValueError("Invalid INSERT statement")

#     if not isinstance(update_part[0], str) or not update_part[0].lstrip().upper().startswith("UPDATE"):
#         raise ValueError("Invalid UPDATE statement")

#     insert_str = ""
#     insert_params = None
#     if len(insert_part) == 1:
#         insert_str = insert_part[0]
#     elif isinstance(insert_part[1], dict):
#         insert_str, insert_params = prepare_sql_text(
#             insert_part[0], insert_part[1], db_type)
#     else:
#         raise ValueError("Invalid insert parameters")

#     update_str = ""
#     update_params = None
#     if len(update_part) == 1:
#         update_str = update_part[0]
#     elif isinstance(update_part[1], dict):
#         update_str, update_params = prepare_sql_text(
#             update_part[0], update_part[1], db_type)
#     else:
#         raise ValueError("Invalid update parameters")

#     result_str = insert_str + \
#         " ON CONFLICT (" + ", ".join(key_fields) + ") DO " + update_str
#     if insert_params is not None and update_params is not None:
#         return result_str, tuple(insert_params) + tuple(update_params)


# def query_helper(connection: Connection, db_type: DbType, mode: QueryMode, sql_text: str, params: dict = None, fetch_one: bool = False, dict_result: bool = False):
#     """Executes SQL query

#     Args:
#         mode (str): Mode for executing query: "select", "insert", "update", "delete", "upsert"
#         sql_text (str): SQL query for execution, parameters indicated with ':' (e.g. ':param')
#         params (dict, optional): Dict of {key: value} where key is matched in sql_text
#         key_fields (tuple, optional): "upsert" mode required: DB table unique fields for UPSERT match (tuple of strings, can be parameters from params)
#         fetch_one (bool, optional): "select" mode optional
#         dict_result (bool, optional): "select" mode optional, returning dictionary type result
#     """

#     if mode not in QueryMode:
#         print("Invalid query mode")
#         return None

#     if not connection:
#         print("No connection...")
#         return None

#     # todo: split by ;

#     try:
#         start_text = sql_text.lstrip().upper()

#         # UPSERT mode
#         if mode == QueryMode.UPSERT and start_text.startswith("INSERT INTO"):
#             pass
#             # if not key_fields:
#             #     raise Exception("No key fields provided for upsert query.")

#             # sql_text = sql_text.strip().rstrip(";")
#             # match = re.search(r"\((.*?)\)\s*VALUES", sql_text,
#             #                   re.IGNORECASE | re.DOTALL)
#             # if not match:
#             #     raise Exception(
#             #         "Cannot parse column list from INSERT statement.")

#             # all_columns = [col.strip() for col in match.group(1).split(",")]
#             # update_columns = [
#             #     col for col in all_columns if col not in key_fields]
#             # if not update_columns:
#             #     raise Exception("No columns to update (all are key fields).")

#             # upsert_suffix = (
#             #     f" ON CONFLICT ({', '.join(key_fields)}) DO UPDATE SET "
#             #     + ", ".join([f"{col} = excluded.{col}" for col in update_columns])
#             # )
#             # sql_text += upsert_suffix

#         elif not start_text.startswith(mode.value.upper()):
#             raise Exception("Query statement and mode inconsistent")

#         # Postgres: append RETURNING for new id
#         if mode == QueryMode.INSERT and db_type == DbType.POSTGRES:
#             sql_text = sql_text.strip().rstrip(";") + " RETURNING id;"

#         # Get cursor
#         if dict_result and mode == QueryMode.SELECT:
#             if db_type == DbType.POSTGRES:
#                 cursor = connection.cursor(cursor_factory=RealDictCursor)
#             elif db_type == DbType.SQLITE:
#                 connection.row_factory = sqlite3.Row
#                 cursor = connection.cursor()
#         else:
#             cursor = connection.cursor()

#         # Execute
#         if params is None:
#             cursor.execute(sql_text)
#         else:
#             sql_text, value_list = prepare_sql_text(sql_text, params, db_type)
#             cursor.execute(sql_text, tuple(value_list))

#         # Handle results
#         if mode == QueryMode.SELECT:
#             rows = cursor.fetchone() if fetch_one else cursor.fetchall()

#             if dict_result and db_type == DbType.SQLITE:
#                 # Convert sqlite3.Row to dict
#                 if rows is None:
#                     return None
#                 if fetch_one:
#                     return dict(rows)
#                 return [dict(row) for row in rows]

#             return rows

#         elif mode == QueryMode.INSERT:
#             if db_type == DbType.POSTGRES:
#                 new_id = cursor.fetchone()[0]
#             elif db_type == DbType.SQLITE:
#                 new_id = cursor.lastrowid
#             connection.commit()
#             return new_id

#         else:  # UPDATE / DELETE / UPSERT
#             connection.commit()

#     except Exception as e:
#         connection.rollback()
#         raise Exception("Error on executing query:", e)
