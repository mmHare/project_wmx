import json
from copy import deepcopy
import sys

from src.globals.glob_enums import DbKind
from src.globals.glob_constants import *
from src.globals.help_functions import encrypt_data


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
    CONF_GENERAL: {},
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
                self.config = json.load(file)

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
