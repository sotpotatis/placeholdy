"""configuration_file.py
Contains utilities for loading and parsing the configuration file."""
import json5
from .paths import CONFIGURATION_FILE_PATH


def get_configuration_file()->dict:
    """Retrieves the contents of the configuration file."""
    return json5.loads(open(CONFIGURATION_FILE_PATH, "r").read())


def update_configuration_file(new_content:dict):
    """Updates the configuration file.

    :param new_content: The full new content of the file as a dictionary."""
    with open(CONFIGURATION_FILE_PATH, "w") as config_file:
        config_file.write(json5.dumps(new_content))
