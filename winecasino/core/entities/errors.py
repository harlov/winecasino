class GameAlreadyStartedError(Exception):
    pass


class GameAlreadyStoppedError(Exception):
    pass


class GameNotStartedError(Exception):
    pass


class NoEnoughPlayersInTheGameError(Exception):
    def __init__(self, required):
        self.required = required


class NoEnoughRoundsInTheGameError(Exception):
    def __init__(self, required):
        self.required = required


class PlayerAlreadyExistsError(Exception):
    pass


class PlayerNotFound(Exception):
    pass


class PlayerAlreadyPlacedBidError(Exception):
    pass


class NoEnoughMoneyForBid(Exception):
    pass


class NoActiveRoundError(Exception):
    pass


class RoundIsEndedError(Exception):
    pass


class RoundIsStillActiveError(Exception):
    pass
