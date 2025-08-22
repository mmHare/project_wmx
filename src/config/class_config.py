from enum import Enum
import json
from copy import deepcopy
import sys

from src.globals.glob_enums import CsvDelimeter, DbKind
from src.globals.glob_constants import *
from src.globals.help_functions import encrypt_data, get_delim


# set of config keys that should be shown hidden
SENSITIVE_CONFIG_KEYS = {
    CONF_DB_L_USER,
    CONF_DB_L_PASS,
    CONF_DB_C_USER,
    CONF_DB_C_PASS
}


# key paths with encrypted values
ENCRYPTED_KEY_PATHS = {
    (CONF_DATABASE, CONF_DB_LOCAL, CONF_DB_L_USER),
    (CONF_DATABASE, CONF_DB_LOCAL, CONF_DB_L_PASS),
    (CONF_DATABASE, CONF_DB_CENTRAL, CONF_DB_C_USER),
    (CONF_DATABASE, CONF_DB_CENTRAL, CONF_DB_C_PASS)
}

config_defaults = {
    CONF_GENERAL: {
        CONF_CSV_DELIM: CsvDelimeter.COMMA,
        CONF_USE_DIALOGS: True
    },
    CONF_DATABASE: {
        CONF_DB_KIND: DbKind.NONE.value,
        CONF_DB_LOCAL: {
            CONF_DB_L_NAME: DB_NAME + ".db",
            CONF_DB_L_PATH: DB_FILE_DIR,
            CONF_DB_L_USER: encrypt_data(""),
            CONF_DB_L_PASS: encrypt_data("")
        },
        CONF_DB_CENTRAL: {
            CONF_DB_C_NAME: DB_NAME,
            CONF_DB_C_HOST: "192.168.0.11",
            CONF_DB_C_PORT: 5432,
            CONF_DB_C_USER: encrypt_data(""),
            CONF_DB_C_PASS: encrypt_data("")
        }
    }
}


class ConfigManager:
    """Class to manage configuration settings."""

    def __init__(self):
        self.config = config_defaults
        self.config_file_path = CONFIG_FILE_PATH

    @property
    def get_csv_delim(self) -> str:
        return get_delim(self.config[CONF_GENERAL][CONF_CSV_DELIM])

    @property
    def is_use_dialogs(self) -> bool:
        return self.config[CONF_GENERAL][CONF_USE_DIALOGS]

    def check_config_structure(self, defaults: dict, conf: dict) -> dict:
        """Recursively checks if config has all keys and adds missing ones with defaults."""
        for key, value in defaults.items():
            if key not in conf:
                # Copy the whole default value (not just None)
                conf[key] = value if not isinstance(
                    value, dict) else value.copy()
            elif isinstance(value, dict) and isinstance(conf[key], dict):
                self.check_config_structure(value, conf[key])
        return conf

    def apply_defaults(self, template: dict, target: dict) -> dict:
        """
        Ensure target dict has same structure as template.
        - Adds missing keys with template values
        - Converts values to Enums if template expects Enum
        """
        for key, default_val in template.items():
            if key not in target:
                target[key] = default_val
            else:
                # If both are dicts → recurse
                if isinstance(default_val, dict) and isinstance(target[key], dict):
                    target[key] = self.apply_defaults(default_val, target[key])

                # If default is Enum type → coerce into Enum
                elif isinstance(default_val, Enum):
                    enum_type = type(default_val)
                    if not isinstance(target[key], enum_type):
                        target[key] = enum_type(target[key])
        return target

    def serialize_enums(self, data: dict) -> dict:
        """
        Recursively replace Enum members in a dict with their .value
        """
        result = {}
        for key, val in data.items():
            if isinstance(val, Enum):
                result[key] = val.value
            elif isinstance(val, dict):
                result[key] = self.serialize_enums(val)
            else:
                result[key] = val
        return result

    def load_config(self):
        self.config = self.load_config_from_file(self.config_file_path)
        if not self.config:
            if input("Error loading configuration. Do you want to use defaults? (y/n): ") == 'y':
                self.config = config_defaults
                self.save_config()
            else:
                print("Failed to load configuration. Exiting...")
                sys.exit()

    def load_config_from_file(self, file_path):
        """Load configuration from file."""
        try:
            with open(file_path, encoding="UTF-8") as file:
                conf = json.load(file)
                self.config = self.apply_defaults(
                    config_defaults, conf)

            # values that should be encrypted
            for section, subsection, key in ENCRYPTED_KEY_PATHS:
                val = self.config[section][subsection][key]
                if isinstance(val, str):
                    self.config[section][subsection][key] = val.encode()

            return self.config
        except FileNotFoundError:
            print("Configuration file not found.")
            return None
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return None

    def save_config(self):
        """Save configuration to file."""
        try:
            config_to_save = deepcopy(self.config)
            config_to_save = self.serialize_enums(config_to_save)
            # values that are encrypted
            for section, subsection, key in ENCRYPTED_KEY_PATHS:
                val = config_to_save[section][subsection][key]
                if isinstance(val, bytes):
                    config_to_save[section][subsection][key] = val.decode()

            with open(self.config_file_path, "w", encoding="UTF-8") as file:
                json.dump(config_to_save, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving configuration: {e}")


# Instance
_config_manager = None


def get_config_manager():
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
