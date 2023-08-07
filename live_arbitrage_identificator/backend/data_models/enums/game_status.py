from enum import Enum


class GameStatus(Enum):
    """
    Enum to represent the status of a game.

    # Explanation:

    - SCHEDULED: The game has not started yet and is not about to start within the next 15 minutes
    - STARTING_SOON: The game is about to start within the next 15 minutes
    - CANCELED: The game has been canceled for some reason, e.g. weather
    - WITHDRAW: Some participant has withdrawn from the game and the winner is declared as the other participant
    - WALKOVER: One participant is declared the winner without the game being played due to the other participant not showing up or being disqualified
    - RETIRED: One participant retires during the game and the winner is declared as the other participant
    - LIVE: The game is currently live
    - FINISHED: The game has been played and the winner is declared as one of the participants based on the game result
    - WON_BY_SCORE: The game has been played, and the winner is declared based on the final score
    - UNKNOWN: The game status is unknown (this should not happen)
    - MISSING: The game status is missing or not available
    - INTERRUPTED: The game has been interrupted for some reason, e.g. weather
    - AWARDED: The game has been awarded to one of the
    """

    SCHEDULED = "SCHEDULED"
    STARTING_SOON = "STARTING_SOON"
    CANCELED = "CANCELED"
    WITHDRAW = "WITHDRAW"
    WALKOVER = "WALKOVER"
    RETIRED = "RETIRED"
    LIVE = "LIVE"
    FINISHED = "FINISHED"
    WON_BY_SCORE = "WON_BY_SCORE"
    UNKNOWN = "UNKNOWN"
    MISSING = "MISSING"
    INTERRUPTED = "INTERRUPTED"
    AWARDED = "AWARDED"
    POSTPONED = "POSTPONED"
