from enum import Enum


class OutcomeReason(str, Enum):
    """Class to represent the different outcome reasons that are or can be supported by the scraper."""

    WON_BY_SCORE = "WON_BY_SCORE"
    CANCELED_BY_WEATHER = "CANCELED_BY_WEATHER"
    CANCELED_BY_PLAYER = "CANCELED_BY_PLAYER"
