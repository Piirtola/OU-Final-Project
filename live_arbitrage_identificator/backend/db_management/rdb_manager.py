import logging
from enum import Enum
from pathlib import Path
from typing import Any, Set, Tuple, Type


import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor, execute_values
from psycopg2.pool import ThreadedConnectionPool
from pydantic import BaseModel


logger = Logger(
    log_dir="logs/database_manager",
    log_file="database_manager.log",
    log_level=logging.INFO,
)


