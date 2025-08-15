"""Functions for users management"""

import getpass

from .class_user import User
from .class_user_manager import user_manager
from src.help_functions import *


def menu_user_log_in_log_out():
    if user_manager.is_logged:
        user_manager.log_out()
    else:
        user_manager.log_in(
            input("Login: "), getpass.getpass("Password: "))


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
