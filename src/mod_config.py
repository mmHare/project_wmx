from copy import deepcopy
import json

from src.constants import *
from src.enums_and_dicts import *


config_defaults = {
    CONF_GENERAL: {},
    CONF_DATABASE: {
        CONF_DB_KIND: DbKind.NONE.value,
        CONF_DB_LOCAL: {
            CONF_DB_L_NAME: DB_NAME + ".db",
            CONF_DB_L_PATH: DB_FILE_DIR,
            CONF_DB_L_USER: "",
            CONF_DB_L_PASS: ""
        },
        CONF_DB_CENTRAL: {
            CONF_DB_C_NAME: DB_NAME,
            CONF_DB_C_HOST: "192.168.0.11",
            CONF_DB_C_PORT: 5432,
            CONF_DB_C_USER: "db_user",  # szyfrowanie
            CONF_DB_C_PASS: "user"  # szyfrowanie
        }
    }
}


def get_conf_key_name(key: str) -> str:
    """Getting name for display"""
    if key in config_defaults:
        if key == CONF_DB_KIND:
            return "Central/Local"
        else:
            return (f"config.{key}").capitalize()


class ConfigManager:
    """Class to manage configuration settings."""

    def __init__(self):
        self.config = config_defaults

        self.config_file_path = CONFIG_FILE_PATH
        self.config = self.load_config()
        if not self.config:
            if input("Error loading configuration. Do you want to use defaults? (y/n): ") == 'y':
                self.config = config_defaults
                self.save_config()
            else:
                exit("Failed to load configuration. Exiting...")

    def load_config(self):
        """Load configuration from file."""
        try:
            with open(self.config_file_path, encoding="UTF-8") as file:
                self.config = json.load(file)
            return self.config
        except FileNotFoundError:
            print("Configuration file not found.")
            return None
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return None

    def save_config(self):
        """Save configuration to file."""
        with open(self.config_file_path, "w", encoding="UTF-8") as file:
            json.dump(self.config, file, indent=4, ensure_ascii=False)
        try:
            pass
        except Exception as e:
            print(f"Error saving configuration: {e}")


def print_config(config):
    """Print configuration settings."""
    print("Current configuration:")
    for section, settings in config.items():
        print(section.upper())
        for subsection, value in settings.items():
            if isinstance(value, dict):
                print(f"  {get_conf_key_name(subsection)}:")
                for subkey, subvalue in value.items():
                    print(f"    {get_conf_key_name(subkey)}: {subvalue}")
            else:
                print(f"  {get_conf_key_name(subsection)}: {value}")


def change_settings():
    """Change configuration settings."""
    config = deepcopy(config_manager.config)
    while True:
        for i, section in enumerate([key for key in config.keys()]):
            print(f"{i + 1}. {section.capitalize()}")

        choice = input("Select a section to change (or '0' to quit): ").strip()

        if choice == '0':
            break

        # todo:


# global ConfigManager Instance
config_manager = ConfigManager()


def config_menu():
    """Method to display configuration settings."""
    while True:
        print("="*10, "Configuration settings:", "="*10)
        print("1. View current settings")
        print("2. Change settings")
        print("0. Exit")

        choice = input("Select an option: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            print("Current settings:")
            print_config(config_manager.config)
        elif choice == "2":
            print("Change settings:")
            pass  # Implement logic to change settings
        else:
            print("Invalid choice. Please try again.")
