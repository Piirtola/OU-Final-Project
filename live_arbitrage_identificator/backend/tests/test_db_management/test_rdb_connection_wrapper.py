import unittest
from live_arbitrage_identificator.backend.db_management.db_config import DBConfig
from live_arbitrage_identificator.utils.load_env import load_db_env
from live_arbitrage_identificator.backend.db_management.rdb_connection_wrapper import (
    RDBConnectionWrapper,
)  # Make sure to import your RDBConnectionWrapper class
import psycopg2.extensions


class TestRDBConnectionWrapper(unittest.TestCase):
    """
    Simple test case for the RDBConnectionWrapper class.
    """

    @classmethod
    def setUpClass(cls):
        cls.db_config = DBConfig(**load_db_env())

    def test_connection_acquisition(self):
        """
        Test that a connection can be successfully acquired from the pool.
        """
        with RDBConnectionWrapper(self.db_config) as conn:
            self.assertIsNotNone(conn)
            self.assertIsInstance(conn, psycopg2.extensions.connection)

    def test_connection_release(self):
        """
        Test that a connection is released back to the pool after use.
        """
        wrapper = RDBConnectionWrapper(self.db_config)
        with wrapper:
            ...  # acquire and release connection

        # Check that the connection was released
        self.assertIsNone(wrapper.conn)

    def test_connection_error_an_release(self):
        """
        Test that an error is raised when the connection fails, .
        """
        wrapper = RDBConnectionWrapper(self.db_config)
        with self.assertRaises(psycopg2.OperationalError):
            with wrapper:
                raise psycopg2.OperationalError

        self.assertIsNone(wrapper.conn)


if __name__ == "__main__":
    unittest.main()
