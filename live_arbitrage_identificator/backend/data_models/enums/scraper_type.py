from enum import Enum


class ScraperType(str, Enum):
    """Enum representing the different scraper types that are or can be supported by the scraper."""

    ODDSPORTAL = "ODDSPORTAL"
