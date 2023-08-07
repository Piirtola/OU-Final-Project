from pydantic import BaseModel


class DBConfig(BaseModel):
    """
    Represents the configuration for managing database connections.

    Attributes:
        DB_NAME (str): The name of the database.
        DB_USER (str): The username to connect to the database.
        DB_PASSWORD (str): The password to connect to the database.
        DB_HOST (str): The hostname or IP address of the database server.
        DB_PORT (str): The port number to use when connecting to the database server.
        SCHEMA (str): The name of the schema to use.
    """

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    SCHEMA: str
