from pathlib import Path


#######################################################################################################################
# (doctests is not working as the path is different on different machines, change the test path to fix this locally)) #
#######################################################################################################################


def get_project_root_abs_path() -> Path:
    """
    Example:
        >>> get_project_root_abs_path()
        PosixPath('/Users/piirtola/Documents/GitHub/OU-Final-Project/live_arbitrage_identificator')
    """

    root_dir = Path(__file__).parent
    while str(root_dir).endswith("live_arbitrage_identificator") is False:
        root_dir = root_dir.parent

    return root_dir


def get_abs_path_from_relative(rel_path: Path | str) -> Path:
    """
    Returns the absolute path of the file given as a relative path from the root folder of the project source code.

    :param rel_path: A relative path from the root folder of the project src
    :type rel_path: Path or str
    :return: Returns the absolute pathlib.Path object to the file given as arg.

    Example:
        >>> get_abs_path_from_relative("data/test.txt")
        PosixPath('/Users/piirtola/Documents/GitHub/OU-Final-Project/live_arbitrage_identificator/data/test.txt')
    """

    return get_project_root_abs_path().joinpath(rel_path)


def get_abs_path_from_relative_backend(rel_path: Path | str) -> Path:
    """
    Returns the absolute path of the file given as a relative path from the backend's root folder

    Example:
        >>> get_abs_path_from_relative_backend("data/test.txt")
        PosixPath('/Users/piirtola/Documents/GitHub/OU-Final-Project/live_arbitrage_identificator/backend/data/test.txt')

    """
    return get_project_root_abs_path().joinpath("backend", rel_path)
