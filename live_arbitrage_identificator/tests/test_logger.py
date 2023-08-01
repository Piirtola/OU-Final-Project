import logging
import os
import time
import unittest
from pathlib import Path

from live_arbitrage_identificator.utils.logger import Logger
from live_arbitrage_identificator.utils.path_helpers import get_abs_path_from_relative


def dummy_function():
    return "Hello, World!"


def dummy_function_with_exception():
    raise ValueError("Dummy exception")


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.log_dir = get_abs_path_from_relative("tests/test_logs")
        self.log_file = "test.log"
        self.logger = Logger(log_dir=self.log_dir, log_file=self.log_file, log_level=logging.INFO)

    def tearDown(self):
        # Remove the log directory and files
        log_path = Path(self.log_dir)
        if log_path.exists():
            for file in log_path.iterdir():
                file.unlink()
            log_path.rmdir()

    def test_create_log_directory(self):
        print(self.log_dir)
        self.assertTrue(os.path.exists(self.log_dir))

    def test_log_message(self):
        log_msg = "Test log message"
        self.logger.log(logging.INFO, log_msg)
        log_file_path = os.path.join(self.log_dir, f"{os.getpid()}_{self.log_file}")
        log_file_path = get_abs_path_from_relative(log_file_path)
        time.sleep(1)
        with open(log_file_path, "r") as file:
            log_content = file.read()
        self.assertIn(log_msg, log_content)

    def test_log_func_call_decorator(self):
        @self.logger.log_func_call
        def func():
            return dummy_function()

        self.assertEqual(func(), "Hello, World!")

    def test_log_timing_decorator(self):
        @self.logger.log_timing
        def func():
            return dummy_function()

        self.assertEqual(func(), "Hello, World!")

    def test_log_exceptions_decorator(self):
        @self.logger.log_exceptions
        def func():
            return dummy_function_with_exception()

        with self.assertRaises(ValueError):
            func()


if __name__ == "__main__":
    unittest.main()
