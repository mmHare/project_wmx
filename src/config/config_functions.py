"""Functions concerning configuration"""

from copy import deepcopy
import getpass

from src.help_functions import *
from src.config import *
from .class_config import *


def get_conf_key_name(key: str) -> str:
    """Getting name for display"""
    for section in config_defaults:
        for _ in section:
            if key == CONF_DB_KIND:
                return f"Kind ({DbKind.CENTRAL.value}/{DbKind.LOCAL.value})"
            else:
                return (f"{key}").capitalize()


def print_config():
    """Print configuration settings."""
    def print_section(data, indent=0):
        """Print sections and values."""
        for key, value in data.items():
            display_key = get_conf_key_name(key)

            if isinstance(value, dict):
                print(" " * indent + f"{display_key}:")
                print_section(value, indent + 2)
            else:
                if (key in SENSITIVE_CONFIG_KEYS) and value:
                    masked_value = "***"
                else:
                    masked_value = value
                print(" " * indent + f"{display_key}: {masked_value}")

    print("Current configuration:")
    for section, settings in config_manager.config.items():
        print(section.upper())
        print_section(settings, indent=2)


def change_settings_value(setting: tuple):
    """Method verifying and returning value for specific config key"""
    (key, value) = setting
    # database user
    if key in [CONF_DB_L_USER, CONF_DB_C_USER]:
        result = input("User: ")
        result = encrypt_data(result)

    # password
    elif key in [CONF_DB_L_PASS, CONF_DB_C_PASS]:
        result = getpass.getpass("New password: ")
        result = encrypt_data(result)

    # database kind
    elif key == CONF_DB_KIND:
        print(f"{get_conf_key_name(key)}: {value}")
        result = input(
            f"'{DbKind.CENTRAL.value}'/'{DbKind.LOCAL.value}': ").lower()
        if result not in [DbKind.CENTRAL.value, DbKind.LOCAL.value]:
            print(
                f"Error: entered value is not '{DbKind.CENTRAL.value}'/'{DbKind.LOCAL.value}'")
            return None

    # other values
    else:
        print(f"{get_conf_key_name(key)}: {value}")
        result = input("New value: ")

    try:
        result = type(value)(result)
    except Exception as e:
        print(f"Error parsing configuration value: {e}")
        result = value
    return result


def loop_through_settings(config, changes_done: bool = False, base_level: bool = False) -> bool:
    """Menu for changing config keys, loops all config"""
    settings_changed = changes_done
    while True:
        # print sections
        sections = [key for key in config.keys()]
        for i, section in enumerate(sections):
            print(f"{i + 1}. {get_conf_key_name(section).capitalize()}")

        choice = input("Select a section to change (or '0' to quit): ").strip()
        if choice == '0':  # exit settings
            return settings_changed
        elif choice.isdigit() and 0 <= int(choice) - 1 < len(sections):
            # option selected
            selected_key = sections[int(choice) - 1]
            selected_section = config[selected_key]

            if isinstance(selected_section, dict):  # section has items
                print(get_conf_key_name(selected_key))
                settings_changed = loop_through_settings(
                    selected_section, settings_changed)
                if not base_level:
                    return settings_changed
            else:
                conf_value = change_settings_value(
                    (selected_key, config[selected_key]))
                if conf_value:
                    config[selected_key] = conf_value
                    return True
        else:
            print("Wrong option.")


def change_settings():
    """Change configuration settings."""
    config_initial = deepcopy(config_manager.config)

    if loop_through_settings(config_manager.config, base_level=True) == 1:
        if input("Do you want to save changes? ('y' to confirm)") == 'y':
            config_manager.save_config()
        else:
            config_manager.config = deepcopy(config_initial)


def restore_settings():
    if input("Restore to defaults? (y/n)") == "y":
        config_manager.config = deepcopy(config_defaults)
        print("Configuration restored.")
