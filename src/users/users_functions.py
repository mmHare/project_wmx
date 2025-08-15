"""Functions for users management"""

import getpass

from .class_user_manager import user_manager
from src.help_functions import *


def menu_user_log() -> tuple:
    if user_manager.is_logged:
        return "Log out", menu_user_log_out
    else:
        return "Log in", menu_user_log_in


def menu_user_log_in():
    return user_manager.log_in(input("Login: "), getpass.getpass("Password: "))


def menu_user_log_out():
    result = input("Do you really want to log out? (y/n): ")
    if result.strip().lower() == "y":
        return user_manager.log_out()
    return False


def menu_list_users():
    print("Users:")
    usr_list = user_manager.get_login_list()
    for user in usr_list:
        print("-", user.login)


def menu_new_user():
    print("New user")
    login = input("Login: ")
    name = input("Name: ")
    surname = input("Surname: ")
    password = getpass.getpass("Password: ")
    user_manager.add_user(login, name, surname, password)


def menu_delete_user():
    print("Delete user")
    user_manager.delete_user(input("Login: "))


def menu_register_user():
    local_ip = get_local_ip()
    print(f"Register current IP ({local_ip}) ? (y/n)")
    if input().strip().lower() == "y":
        user_manager.register_ip(local_ip)
    else:
        print("IP registration canceled.")


def get_logged_user_info():
    if user_manager.is_logged:
        user = user_manager.logged_user
        return f"Logged user: {user.login} - {user.name} {user.surname}"
    return "No user is logged in."
