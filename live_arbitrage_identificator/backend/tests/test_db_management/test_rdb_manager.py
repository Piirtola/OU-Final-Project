import unittest
from unittest.mock import MagicMock, patch, call
from live_arbitrage_identificator.backend.db_management.rdb_manager import RDBManager
from psycopg2 import sql, extras, errors
from live_arbitrage_identificator.backend.db_management.db_config import DBConfig
from live_arbitrage_identificator.utils.load_env import load_test_db_env
from live_arbitrage_identificator.backend.db_management.rdb_schema_builder import RDBArbitrageSchemaBuilder
from live_arbitrage_identificator.backend.db_management.rdb_connection_wrapper import RDBConnectionWrapper

class TestRDBManager(unittest.TestCase):
    """
    Contains simple mock tests for the RDBManager class.
    Some methods are not tested because of some troubles when trying to mock psycopg2 methods
    that are inside a context manager (e.g. execute_values_query).

    These tests are not needed for now, and we can test these methods with integration tests (see below).
    """

    def setUp(self):
        self.connection_mock = MagicMock()
        self.schema_builder_mock = MagicMock()
        self.rdb_manager = RDBManager(self.connection_mock, self.schema_builder_mock)

    def test_init(self):
        """
        Test that the RDBManager is initialized correctly, and that the schema is built.
        """
        self.schema_builder_mock.build_schema.assert_called_once_with(query_executor=self.rdb_manager)

    @patch.object(RDBManager, 'execute_query')
    def test_execute_query(self, mock_execute_query):
        """
        Test that the execute_query method sets the search path and executes the query.
        """
        query = sql.SQL("SELECT * FROM table")
        params = ("param1", "param2")
        fetch = True

        self.rdb_manager.execute_query(query, params, fetch)

        mock_execute_query.assert_called_once_with(query, params, fetch)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="SELECT * FROM table")
    @patch.object(RDBManager, 'execute_query')
    def test_run_a_script_file(self, mock_execute_query, mock_open):
        """
        Test that the run_a_script_file method correctly handles script file execution.
        """
        self.rdb_manager.run_a_script_file('path/to/file')
        mock_open.assert_called_once_with('path/to/file', 'r')
        mock_execute_query.assert_called_once_with('SELECT * FROM table')


class TestIntegrationRDBManager(unittest.TestCase):
    """
    Contains integration tests for the RDBManager class.
    Note, these tests use the real database, and therefore require a database to be running.
    Also note that these tests can break the real DB if the tests are messed with.

    """
    @classmethod
    def setUpClass(cls):
        cls.config = DBConfig(**load_test_db_env())
        cls.connection_wrapper = RDBConnectionWrapper(cls.config)
        cls.schema_builder = RDBArbitrageSchemaBuilder()

    def setUp(self):
        self.rdb_manager = RDBManager(self.connection_wrapper, self.schema_builder)

    def test_database_connection(self):
        self.assertIsNotNone(self.rdb_manager.connection_wrapper.connection())

    def test_table_not_exists_error(self):
        """
        Tests that if a table does not exist the psycopg2.errors.UndefinedTable error is raised.
        """
        query = sql.SQL("SELECT * FROM table_that_does_not_exist")
        with self.assertRaises(errors.UndefinedTable) as context:
            self.rdb_manager.execute_query(query, fetch=True)
        self.assertEqual(context.exception.pgcode, "42P01")





if __name__ == "__main__":
    unittest.main()
