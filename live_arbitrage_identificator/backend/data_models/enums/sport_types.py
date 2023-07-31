from enum import Enum


class SportType(str, Enum):
    """Enum representing the different sport types that are or can be supported by the scraper. To edit the supported sports, edit the config YAML file."""

    TENNIS = "TENNIS"
    TABLE_TENNIS = "TABLE_TENNIS"
    # BASKETBALL = "BASKETBALL"
