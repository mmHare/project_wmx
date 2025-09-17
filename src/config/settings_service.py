"""Functions concerning configuration"""

from copy import deepcopy
import getpass
from tkinter import Tk, filedialog

import distutils

from src.globals.glob_constants import *
from src.globals.glob_enums import *
from src.globals.help_functions import *
from src.config.config_manager import get_config_manager, config_defaults, SENSITIVE_CONFIG_KEYS


class SettingsService:
    _config_manager = get_config_manager()

    @staticmethod
    def __get_conf_key_name(key: str) -> str:
        """Getting config key name for display"""
        for section in config_defaults:
            for _ in section:
                if key == CONF_DB_KIND:
                    return f"Kind ({DbKind.CENTRAL.value}/{DbKind.LOCAL.value})"
                elif key == CONF_CSV_DELIM:
                    return "CSV delimeter"
                elif key == CONF_USE_DIALOGS:
                    return "Use dialogs"
                elif key == CONF_LOG_PATH:
                    return "Path to log files"
                else:
                    return (f"{key}").capitalize()

    @classmethod
    def load_config(cls):
        return cls._config_manager.load_config()

    @classmethod
    def change_settings_value(cls, setting: tuple):
        """Method verifying and returning value for specific config key. 
        setting (key, value)"""
        (key, value) = setting
        try:
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
                print(f"{cls.__get_conf_key_name(key)}: {value}")
                result = input(
                    f"'{DbKind.CENTRAL.value}'/'{DbKind.LOCAL.value}': ").lower()
                if result not in [DbKind.CENTRAL.value, DbKind.LOCAL.value]:
                    raise ValueError(
                        f"Entered value is not '{DbKind.CENTRAL.value}'/'{DbKind.LOCAL.value}'")

            # paths selection using dialogs
            elif cls._config_manager.config[CONF_GENERAL][CONF_USE_DIALOGS] and key in [CONF_DB_L_PATH, CONF_LOG_PATH]:
                print("Please select new path: ")
                root = Tk()
                root.withdraw()  # hide main window
                root.update()
                root.attributes("-topmost", True)  # Force on top
                root.focus_force()
                path = filedialog.askdirectory(initialdir=value)
                root.destroy()
                result = path if path else value

            # enum with int values | key in [CONF_CSV_DELIM]:
            elif issubclass(type(value), Enum) and (isinstance(value.value, int)):
                print(f"{cls.__get_conf_key_name(key)}: {value}")
                for val in type(value):
                    print(f"{val.value}. {str(val).capitalize()}")
                result = int(input("New value (select option): "))

            # other values
            else:
                print(f"{cls.__get_conf_key_name(key)}: {value}")
                result = input("New value: ")
                if isinstance(value, bool):
                    result = bool(distutils.util.strtobool(result))

                result = type(value)(result)
        except Exception as e:
            print(f"Error parsing configuration value: {e}")
            result = value
        return result

    @classmethod
    def __loop_through_settings(cls, config, changes_done: bool = False, base_level: bool = False) -> bool:
        """Menu for changing config keys, loops all config"""
        settings_changed = changes_done
        while True:
            # print sections
            sections = [key for key in config.keys()]
            for i, section in enumerate(sections):
                print(f"{i + 1}. {cls.__get_conf_key_name(section).capitalize()}")

            choice = input(
                "Select a section to change (or '0' to quit): ").strip()
            if choice in ['0', 'q']:  # exit settings
                return settings_changed
            elif choice.isdigit() and 0 <= int(choice) - 1 < len(sections):
                # option selected
                selected_key = sections[int(choice) - 1]
                selected_section = config[selected_key]

                if isinstance(selected_section, dict):  # section has items
                    print(cls.__get_conf_key_name(selected_key))
                    settings_changed = cls.__loop_through_settings(
                        selected_section, settings_changed)
                    if not base_level:
                        return settings_changed
                else:
                    conf_value = cls.change_settings_value(
                        (selected_key, config[selected_key]))
                    if conf_value is not None:
                        config[selected_key] = conf_value
                        return True
            else:
                print("Wrong option.")

    @classmethod
    def change_settings(cls):
        """Change configuration settings."""
        initial_db_kind = cls._config_manager.config[CONF_DATABASE][CONF_DB_KIND]
        config_initial = deepcopy(cls._config_manager.config)

        if cls.__loop_through_settings(cls._config_manager.config, base_level=True) == 1:
            if input("Do you want to save changes? ('y' to confirm)") == 'y':
                cls._config_manager.save_config()
            else:
                cls._config_manager.config = deepcopy(config_initial)
        return cls._config_manager.config[CONF_DATABASE][CONF_DB_KIND] != initial_db_kind

    @classmethod
    def restore_settings(cls):
        if input("Restore to defaults? (y/n)") == "y":
            cls._config_manager.config = deepcopy(config_defaults)
            print("Configuration restored.")

    @classmethod
    def print_config(cls):
        """Print configuration settings."""
        def print_section(data, indent=0):
            """Print sections and values."""
            for key, value in data.items():
                display_key = cls.__get_conf_key_name(key)

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
        for section, settings in cls._config_manager.config.items():
            print(section.upper())
            print_section(settings, indent=2)

    @classmethod
    def save_to_log(cls, msg: str):
        save_to_log_file(cls._config_manager.config[CONF_LOG_PATH], msg)

    @classmethod
    def clear_logs(cls):
        delete_log_files(cls._config_manager.config[CONF_LOG_PATH])

    @classmethod
    def load_last_log(cls) -> str:
        return load_last_log_file(cls._config_manager.config[CONF_LOG_PATH])
