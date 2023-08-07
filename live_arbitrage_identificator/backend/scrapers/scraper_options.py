from enum import Enum


class SCRAPER_TYPE(str, Enum):
    """
    Tracks all the available scrapers to enhance the code extensibility.
    """

    ODDSPORTAL = "ODDSPORTAL"


class SCRAPER_DATA_TYPE(Enum):
    """
    Tracks the type of data that the scraper is going to scrape, as some sites have different pages for metadata and data.
    """

    METADATA = "METADATA"
    DATA = "DATA"
