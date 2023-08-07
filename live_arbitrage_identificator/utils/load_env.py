import os.path
from typing import Dict, Tuple
from enum import Enum
import decouple
from typing import Optional


class EnvFileType(Enum):
    """Simple Enum Class to help with the choose between the .env and .env.test files."""
    ENV = ".env"
    ENV_TEST = ".env.test"


def load_env_variables(variables: Tuple[str, ...], env_file_type: Optional[EnvFileType] = EnvFileType.ENV) -> Dict[str, str]:
    """
    Load environment variables from the .env file.

    Args:
        variables (Tuple[str, ...]): A tuple containing the environment variable names to be loaded.
        env_file_type (EnvFileType, optional): The type of .env file to be loaded. Defaults to EnvFileType.ENV.

    Returns:
        Dict[str, str]: A dictionary containing the environment variable names and their respective values.

    Raises:
        decouple.UndefinedValueError: If any of the specified environment variables are not found in the .env file.
    """
    config = decouple.AutoConfig(search_path=os.path.realpath(env_file_type.name))
    env_vars = {}
    try:
        for var in variables:
            env_vars[var] = config(var)
        print(f"Successfully loaded the credentials `{variables}` from the .env file")
    except decouple.UndefinedValueError as e:
        print("The .env file is not configured appropriately!")
        raise e

    return env_vars


def load_db_env() -> Dict[str, str]:
    """
    Load database environment variables from the .env file.

    Returns:
        Dict[str, str]: A dictionary containing the database environment variable names and their respective values.
    """
    db_variables = ("DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "SCHEMA")
    return load_env_variables(db_variables)


def load_oddsportal_env() -> Tuple[str, str]:
    """
    Load the credentials to oddsportal.com from the .env file.

    Returns:
        Tuple[str, str]: A tuple containing the username and PASSWORD for oddsportal.com.
    """
    oddsportal_variables = ("ODDSPORTAL_USER", "ODDSPORTAL_PASSWORD")
    oddsportal_credentials = load_env_variables(oddsportal_variables)

    return (
        oddsportal_credentials["ODDSPORTAL_USER"],
        oddsportal_credentials["ODDSPORTAL_PASSWORD"],
    )
