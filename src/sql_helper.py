"""Reusable universal SQL query handlers for Postgre and SQLite"""

import re
from sqlite3 import Connection
import sqlite3
from psycopg2.extras import RealDictCursor

from src.globals import *


def prepare_sql_text(sql_text: str, params: dict, db_type: DbType) -> tuple[str, tuple]:
    """
    Formats sql_text with parameters starting with ':' (e.g. ':par') for given DB type.
    Parameters are matched against `params` dict of param_name -> value.
    Returns formatted SQL text and tuple of values in order of occurrence.
    """
    if db_type not in (DbType.POSTGRES, DbType.SQLITE):
        raise ValueError("Database not supported")

    placeholder = "%s" if db_type == DbType.POSTGRES else "?"
    values = []

    def replacer(match: re.Match) -> str:
        name = match.group(1)  # the part after ':'
        if name not in params:
            raise ValueError(f"Missing parameter: {name}")
        values.append(params[name])
        return placeholder

    # regular to find parameters :param_name
    sql_text = re.sub(r":(\w+)", replacer, sql_text)
    return sql_text, tuple(values)


def query_helper(connection: Connection, db_type: DbType, mode: QueryMode, sql_text: str, params: dict = None, key_fields: tuple = None, fetch_one: bool = False, dict_result: bool = False):
    """Executes SQL query

    Args:
        mode (str): Mode for executing query: "select", "insert", "update", "delete", "upsert"
        sql_text (str): SQL query for execution, parameters indicated with ':' (e.g. ':param')
        params (dict, optional): Dict of {key: value} where key is matched in sql_text
        key_fields (tuple, optional): "upsert" mode required: DB table unique fields for UPSERT match (tuple of strings, can be parameters from params)
        fetch_one (bool, optional): "select" mode optional
        dict_result (bool, optional): "select" mode optional, returning dictionary type result
    """

    if mode not in QueryMode:
        print("Invalid query mode")

    if connection:
        try:
            """preparing text"""
            start_text = sql_text.lstrip().upper()

            if (mode == QueryMode.UPSERT) and start_text.startswith(("INSERT INTO")):
                if key_fields is None:
                    raise Exception("No key fields provided for upsert query.")

                sql_text = sql_text.strip().rstrip(";")
        # ChatGPT generated
                # Extract column list from INSERT INTO table_name (col1, col2, ...)
                match = re.search(r"\((.*?)\)\s*VALUES", sql_text,
                                  re.IGNORECASE | re.DOTALL)
                if not match:
                    raise Exception(
                        "Cannot parse column list from INSERT statement.")

                all_columns = [col.strip()
                               for col in match.group(1).split(",")]
                update_columns = [
                    col for col in all_columns if col not in key_fields]

                if not update_columns:
                    raise Exception(
                        "No columns to update (all are key fields).")

                upsert_suffix = (
                    f" ON CONFLICT ({', '.join(key_fields)}) DO UPDATE SET "
                    + ", ".join([f"{col} = excluded.{col}" for col in update_columns])
                )
        ####
                sql_text += upsert_suffix

            elif not start_text.startswith(mode.value.upper()):
                raise Exception(
                    "Query statement and mode inconsistent")

            if mode == QueryMode.INSERT:
                # edit for returning new record id
                if db_type == DbType.POSTGRES:
                    sql_text = sql_text.strip().rstrip(";")
                    sql_text += "RETURNING id;"

            """get cursor"""
            if dict_result and (mode == QueryMode.SELECT):  # returns dict
                if db_type == DbType.POSTGRES:
                    cursor = connection.cursor(cursor_factory=RealDictCursor)

                elif db_type == DbType.SQLITE:
                    cursor = connection.cursor()
                    cursor.row_factory = sqlite3.Row
            else:
                cursor = connection.cursor()

            """execute"""
            if params is None:
                cursor.execute(sql_text)
            else:
                sql_text, value_list = prepare_sql_text(
                    sql_text, params, db_type)
                cursor.execute(sql_text, tuple(value_list))

            if mode == QueryMode.SELECT:
                if fetch_one:
                    return cursor.fetchone()
                else:
                    return cursor.fetchall()
            if mode == QueryMode.INSERT:
                if db_type == DbType.POSTGRES:
                    new_id = cursor.fetchone()[0]

                elif db_type == DbType.SQLITE:
                    new_id = cursor.lastrowid

                connection.commit()
                return new_id
            else:
                connection.commit()

        except Exception as e:
            connection.rollback()
            print("Error on executing query:", e)
            return None
    else:
        print("No connection...")
        return None
