import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from live_arbitrage_identificator.utils.path_helpers import get_abs_path_from_relative


class InvalidConfigurationException(Exception):
    """Exception raised when the configuration file is invalid."""


class ConfigManager:
    """A utility class for managing configuration files."""

    def __init__(self, filename: str = "config.yaml"):
        """Initialize the ConfigManager with the given configuration file.

        :param filename: The name of the configuration file.
        """
        self.path = get_abs_path_from_relative("config/" + filename)
        self.config = self._read_yaml_file(self.path)

    def _read_yaml_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Read the contents of a YAML file.

        :param file_path: The path to the YAML file.
        :return: The contents of the YAML file as a dictionary, or None if an error occurred.
        """
        yaml_content = None
        with file_path.open("r") as file:
            try:
                yaml_content = yaml.safe_load(file)
            except yaml.YAMLError as e:
                logging.error(f"Error loading YAML file: {e}")
                raise InvalidConfigurationException(f"Failed to load configuration file: {file_path}")
        if type(yaml_content) != dict:
            raise InvalidConfigurationException(f"Invalid configuration format in file: {file_path}")

        return yaml_content

    @lru_cache
    def get_config(self, key: str) -> Any:
        """Get the value of a specified key from the loaded configuration.

        :param key: The key to get the value of.
        :return: The value of the specified key, or None if the key is not found.
        """
        value = os.environ.get(key, self.config.get(key))
        return value

    def load_referenced_yaml(self, key: str) -> Optional[Dict[str, Any]]:
        """Load the contents of a referenced YAML file.

        :param key: The key for the file path of the referenced YAML file.
        :return: The contents of the referenced YAML file as a dictionary, or None if the key is not found or an error occurred.
        """
        file_path = self.config.get(key)
        if file_path:
            return self._read_yaml_file(get_abs_path_from_relative(file_path))
        return None

    def reload(self):
        """Reload the configuration file."""
        self.config = self._read_yaml_file(self.path)
        self.get_config.cache_clear()  # Clear the cache for the get_config method


if "__name__" == "__main__":
    # Tests the ConfigManager class
    config_manager = ConfigManager()
    print(config_manager.get_config("test_key"))
