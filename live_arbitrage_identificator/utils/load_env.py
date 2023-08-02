from typing import Dict, Tuple

import decouple


def load_env_variables(variables: Tuple[str, ...]) -> Dict[str, str]:
    """
    Load environment variables from the .env file.

    Args:
        variables (Tuple[str, ...]): A tuple containing the environment variable names to be loaded.

    Returns:
        Dict[str, str]: A dictionary containing the environment variable names and their respective values.

    Raises:
        decouple.UndefinedValueError: If any of the specified environment variables are not found in the .env file.
    """
    config = decouple.AutoConfig()
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
    db_variables = ("DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT")
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
