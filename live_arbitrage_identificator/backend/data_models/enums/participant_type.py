from enum import Enum


class ParticipantType(Enum):
    """Enum representing the different participant types that are or can be supported by the scraper."""

    PLAYER = "PLAYER"
    TEAM = "TEAM"
    PLAYER_PAIR = "PLAYER_PAIR"
    UNKNOWN = "UNKNOWN"
    MISSING = "MISSING"
