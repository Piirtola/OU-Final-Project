from typing import Type, Set
from enum import Enum


def get_current_enum_values(enum_class: Type[Enum]) -> Set[str]:
    """
    Get the current values of an Enum class.

    Args:
        enum_class (Type[Enum]): The Python Enum class to retrieve the values from.

    Returns:
        Set[str]: A set of the current values of the Enum class.

    Doctest:
    >>> from enum import Enum
    >>> class TestEnum(Enum):
    ...     VAL1 = 1
    ...     VAL2 = 2
    >>> sorted(list(get_current_enum_values(TestEnum)))
    ['VAL1', 'VAL2']
    """
    return set(member.name for member in enum_class)
