import logging
import os
import time
from functools import wraps
from logging.handlers import RotatingFileHandler
from queue import Queue
from threading import Thread

from live_arbitrage_identificator.utils.path_helpers import get_abs_path_from_relative


class Logger:
    def __init__(
        self,
        log_dir="logs",
        log_file="app.log",
        log_level=logging.DEBUG,
        log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(module)s - %(funcName)s - %(lineno)d - %(process)d",
    ):
        """
        A utility class for logging supporting multi-threading including a decorator to log function calls.

        :param log_dir: The directory to store log files.
        :param log_file: The name of the log file.
        :param log_level: The logging level.
        :param log_format: The logging format.
        :return: None
        """
        self.log_dir = get_abs_path_from_relative(log_dir)
        self.log_file = log_file
        self.log_level = log_level
        self.log_format = log_format

        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_level)

        self.formatter = logging.Formatter(self.log_format)

        self.create_log_directory()
        self.add_file_handler()
        self.add_stream_handler()

        self.queue = Queue()
        self.thread = Thread(target=self._log_worker)
        self.thread.daemon = True
        self.thread.start()

    def create_log_directory(self):
        """Create the log directory if it doesn't exist."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def add_file_handler(self):
        """Add a file handler to the logger."""
        log_file_path = os.path.join(
            self.log_dir, f"{os.getpid()}_{self.log_file}"
        )  # Adding process id to the file name
        file_handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=3)
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def add_stream_handler(self):
        """Add a stream handler to the logger."""
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.log_level)
        stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(stream_handler)

    def log(self, level, msg):
        """Add a log message to the queue."""
        self.queue.put((level, msg))

    def _log_worker(self):
        """Worker thread to handle logging."""
        while True:
            level, msg = self.queue.get()
            self.logger.log(level, msg)
            self.queue.task_done()

    def log_func_call(self, func):
        """A decorator to log function calls."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            self.log(logging.INFO, f"Calling function: {func_name}")
            result = func(*args, **kwargs)
            self.log(logging.INFO, f"Function {func_name} executed successfully")
            return result

        return wrapper

    def log_timing(self, func):
        """A decorator to log the execution time of a function."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            func_name = func.__name__
            self.log(
                logging.INFO,
                f"Function {func_name} took {execution_time:.2f} seconds to execute",
            )
            return result

        return wrapper

    def log_exceptions(self, func):
        """A decorator to log any exceptions that occur within a function."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.log(logging.ERROR, f"Exception occurred in {func.__name__}: {e}")
                raise

        return wrapper
