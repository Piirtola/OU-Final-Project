from psycopg2.pool import ThreadedConnectionPool
from psycopg2 import Error
import psycopg2.extensions

from live_arbitrage_identificator.backend.db_management.db_config import DBConfig

class RDBConnectionWrapper:
    """
    Wrapper class for managing connections to a relational database (RDB) using connection pooling.

    This class leverages psycopg2's `ThreadedConnectionPool` to maintain a pool of connections to the database,
    optimizing resource utilization and performance. The connection pool's size can be controlled by adjusting
    the `minconn` and `maxconn` parameters.

    The context management protocol is implemented, allowing the use of the `with` statement to manage
    connections, ensuring proper acquisition and release of connections from the pool.

    x = RDBConnectionWrapper(config)
     -> Initializes the connection pool with the provided configuration parameters.

    Params:
        config (DBConfig): An instance of DBConfig containing the necessary configuration parameters
            for connecting to the database, including database name, user, password, host, and port.

    Attributes:
        pool (ThreadedConnectionPool): The connection pool for managing connections to the database.
        conn (Optional[psycopg2.extensions.connection]): The current active connection, if any.
        config (DBConfig): The configuration parameters for connecting to the database.
    """

    def __init__(self, config: DBConfig):
        self.config = config
        self.pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT,
        )
        self.conn = None

    def __enter__(self) -> psycopg2.extensions.connection:
        """
        Acquires a connection from the connection pool and returns it.

        Raises:
            ConnectionError: If there is a failure in establishing the connection to the database.

        Returns:
            psycopg2.extensions.connection: The acquired connection.
        """
        try:
            self.conn = self.pool.getconn()
            return self.conn
        except Error as e:
            raise ConnectionError(f"Failed to connect to the database: {str(e)}") from e

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Releases the acquired connection back to the connection pool.

        This method ensures that connections are returned to the pool when no longer needed,
        maintaining the efficiency and integrity of the pool.
        """
        self.pool.putconn(self.conn)
        self.conn = None
