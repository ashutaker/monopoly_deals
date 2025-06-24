class CustomError(Exception):
    default_message = "Unhandled exception"

    def __init__(self, message: str = None):
        super().__init__(message or self.default_message)


class NotYourTurn(CustomError):
    default_message = f"Its not your turn"


class GameNotInProgress(CustomError):
    default_message = "Game is not in progress"


class InvalidPlayer(CustomError):
    default_message = f"Player not found in the game"


class InvalidCard(CustomError):
    default_message = "Card not found in your hand"


class InvalidCard(CustomError):
    default_message = "Card not found in your hand"

class NoPropertyColor(CustomError):
    default_message = "Property color must be specified"

class InValidPropertyColor(CustomError):
    default_message = "Incorrect property color must be specified"
