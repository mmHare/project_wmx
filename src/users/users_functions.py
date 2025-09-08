"""Functions for users management"""

import getpass

from src.globals import UserRole, get_local_ip
from .users_conversation import Conversation
from .class_user import User
from .class_user_manager import get_user_manager
from src.database.class_connection_manager import get_connection_manager

user_manager = get_user_manager()
connection_manager = get_connection_manager()

# Menu function tuples


def menu_user_log_in_if_visible() -> tuple:
    if connection_manager.connection and not user_manager.is_logged:
        return "Log in", menu_user_log_in
    else:
        return None, None


def menu_register_user() -> tuple:
    if user_manager.is_logged:
        local_ip = get_local_ip()
        return f"Register IP ({local_ip})", register_user
    else:
        return None, None


# Menu options


def menu_user_log_in():
    return user_manager.log_in(input("Login: "), getpass.getpass("Password: "))


def menu_user_log_out():
    result = input("Do you really want to log out? (y/n): ")
    if result.strip().lower() == "y":
        return user_manager.log_out()
    return False


def log_out_silent():
    user_manager.log_out()
    return user_manager.is_logged


def menu_list_users():
    print("Users:")
    for user in user_manager.get_login_list():
        print(
            f"  {user.login} ({user.ip_address if user.ip_address else 'No IP registered'})")


def menu_new_user():
    def validate_text(text):
        if len(text) < 3:
            print("Must be at least 3 characters long.")
            return False
        elif any(c.isspace() for c in text):
            print("Cannot include whitespaces.")
            return False
        elif not text.isalnum():
            print("Login must be alphanumeric.")
            return False
        return True

    print("New user")
    user = User()
    failed_count = 0
    while True:
        login = input("Login: ")
        if login == "q":
            print("Cancelling operation...")
            return
        if validate_text(login):
            if not user_manager.check_if_user_exists(login):
                user.login = login
                break
            else:
                print("User already exists.")
        else:
            failed_count += 1
            if failed_count > 2:
                print("Cancelling operation...")
                return

    user.name = input("Name: ")
    user.surname = input("Surname: ")
    while True:
        password = getpass.getpass("Password: ")
        if validate_text(password):
            break

    while True:
        user_role = input("User role (admin/user): ")
        if user_role in ["admin", "user"]:
            user.user_role = UserRole.ADMIN if user_role == "admin" else UserRole.USER
            break
        print("Invalid role. Please enter 'admin' or 'user'.")

    choice = input(f"Do you want to create user {login}? (y/n): ")
    if choice.strip().lower() == "y":
        user_manager.add_user(user, password)


def menu_delete_user():
    print("Delete user")
    while True:
        login = input("Login: ")
        if login == "":
            return
        if login == user_manager.logged_user.login:
            print("You cannot delete yourself.")
            continue
        if user_manager.check_if_user_exists(login):
            choice = input(f"Do you want to delete user {login}? (y/n): ")
            if choice.strip().lower() == "y":
                user_manager.delete_user(login)
                print(f"User {login} deleted.")
            else:
                print(f"User {login} not deleted.")
        else:
            print(f"User {login} does not exist.")


def menu_user_conversation():
    login = input("Enter login of user to start conversation:")

    if login == "":
        return
    if login == user_manager.logged_user.login:
        print("You cannot choose yourself.")
        return

    if not user_manager.check_if_user_exists(login):
        print(f"User {login} is not available")
        return

    peer_guid = user_manager.get_user_guid(login)
    conversation = Conversation(user_manager.logged_user, peer_guid)
    conversation.start()


def register_user():
    local_ip = get_local_ip()
    print(f"Register current IP ({local_ip})? (y/n)")
    if input().strip().lower() == "y":
        user_manager.register_ip(local_ip)


def get_logged_user_info():
    if user_manager.is_logged:
        user = user_manager.logged_user
        return f"{user.user_role.name.capitalize()}: {user.login} - {user.name} {user.surname}"
    return "No user is logged in."


def get_user_guid(user_id: int | str):
    return user_manager.get_user_guid(user_id)
