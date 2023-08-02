import os
import unittest

from live_arbitrage_identificator.utils.config_manager import ConfigManager, InvalidConfigurationException


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.config_manager = ConfigManager(filename="test_valid_config.yaml")

    def test_read_yaml_file(self):
        # Test that the configuration file is read properly
        self.assertIsNotNone(self.config_manager.config)

    def test_invalid_yaml_file(self):
        # Test with an invalid YAML file
        with self.assertRaises(InvalidConfigurationException):
            ConfigManager(filename="test_invalid_config.yaml")

    def test_get_config(self):
        # Test that the test_key is read properly
        test_key_value = self.config_manager.get_config("test_key")
        self.assertIsNotNone(test_key_value)
        self.assertEqual(test_key_value[0]["test_value"], "This is a string...")

    def test_reload(self):
        # Test reload method
        self.config_manager.reload()
        self.assertIsNotNone(self.config_manager.config)

    def test_get_config_with_env_var(self):
        # Test getting a configuration value from an environment variable
        os.environ["ENV_TEST_KEY"] = "env_test_value"
        self.config_manager.config["ENV_TEST_KEY"] = "config_test_value"
        self.assertEqual(self.config_manager.get_config("ENV_TEST_KEY"), "env_test_value")


if __name__ == "__main__":
    unittest.main()
