import enum
from datetime import datetime
from typing import Optional, ClassVar

from .base import Model, ValueObject, Field, PrivateAttr

from .user import User
from .wine import Wine
from .country import Country
from . import errors


class Bid(ValueObject):
    class Type(enum.IntEnum):
        SUGAR = enum.auto()
        PART_OF_WORLD = enum.auto()
        COUNTRY = enum.auto()
        WINE = enum.auto()

    user: User
    type: Type
    amount: int

    b_sugar: Optional[Wine.Sugar]
    b_part_of_world: Optional[Country.PartOfWorld]
    b_country: Optional[Country]
    b_wine: Optional[Wine]

    def is_matched(self, wine: Wine) -> bool:
        if self.type == self.Type.SUGAR:
            return self.b_sugar == wine.sugar
        elif self.type == self.Type.PART_OF_WORLD:
            return self.b_part_of_world == wine.country.part_of_world
        elif self.type == self.Type.COUNTRY:
            return self.b_country == wine.country
        else:
            return self.b_wine == wine


class QuestItem(ValueObject):
    wine: Wine


class RoundResult(ValueObject):
    user: User
    is_right_answer: bool
    prize: int


class Round(ValueObject):
    is_ended: bool = False

    BID_MULTIPLIER_MAP = {
        Bid.Type.SUGAR: 2,
        Bid.Type.PART_OF_WORLD: 3,
        Bid.Type.COUNTRY: 5,
        Bid.Type.WINE: 10,
    }

    quest_item: QuestItem
    bids: list[Bid] = Field(default_factory=list)

    _results: list[RoundResult] = PrivateAttr(default_factory=list)

    def place_a_bid(self, bid: Bid) -> None:
        if self.is_ended:
            raise errors.RoundIsEndedError

        for b in self.bids:
            if b.user.id == bid.user.id:
                raise errors.PlayerAlreadyPlacedBidError

        self.bids.append(bid)

    def end(self):
        if self.is_ended:
            raise errors.RoundIsEndedError

        for b in self.bids:
            if b.is_matched(self.quest_item.wine):
                r = RoundResult(
                    user=b.user,
                    is_right_answer=True,
                    prize=b.amount + b.amount * self.BID_MULTIPLIER_MAP[b.type],
                )
            else:
                r = RoundResult(user=b.user, is_right_answer=False, prize=0)
            self._results.append(r)

        self.is_ended = True

    def get_result_for_user(self, user: User) -> Optional[RoundResult]:
        if not self.is_ended:
            raise errors.RoundIsStillActiveError()

        for r in self._results:
            if r.user.id == user.id:
                return r
        return None


class PlayerState(ValueObject):
    user: User
    balance: int


class Game(Model):
    MIN_PLAYERS_COUNT: ClassVar[int] = 2
    MIN_ROUNDS_COUNT: ClassVar[int] = 2
    STARTING_BALANCE: ClassVar[int] = 1000

    class State(enum.IntEnum):
        CREATED = enum.auto()
        BEFORE_ROUNDS = enum.auto()
        ROUNDS_PLAYING = enum.auto()
        ALL_ROUNDS_PLAYED = enum.auto()
        ENDED = enum.auto()

    name: str
    rounds: list[Round] = Field(default_factory=list)
    players: list[PlayerState] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    started_at: Optional[datetime]
    stopped_at: Optional[datetime]
    ended_at: Optional[datetime]

    state: State = State.CREATED
    _active_round_idx: int = PrivateAttr()

    def start(self):
        if self.state != self.State.CREATED:
            raise errors.GameAlreadyStartedError

        if len(self.players) < self.MIN_PLAYERS_COUNT:
            raise errors.NoEnoughPlayersInTheGameError(self.MIN_PLAYERS_COUNT)

        if len(self.rounds) < self.MIN_ROUNDS_COUNT:
            raise errors.NoEnoughRoundsInTheGameError(self.MIN_ROUNDS_COUNT)

        self.started_at = datetime.utcnow()
        self._active_round_idx = -1
        self.state = self.State.BEFORE_ROUNDS

    def start_next_round(self) -> bool:
        if self.state == self.State.ALL_ROUNDS_PLAYED:
            return False

        if self.state == self.State.BEFORE_ROUNDS:
            self.state = self.State.ROUNDS_PLAYING

        if self._active_round_idx + 1 > len(self.rounds) - 1:
            self.state = self.State.ALL_ROUNDS_PLAYED
            self._active_round_idx = -1
            return False

        self._active_round_idx += 1
        return True

    def finish_current_round(self):
        if self.state in (self.State.BEFORE_ROUNDS, self.State.ALL_ROUNDS_PLAYED):
            raise errors.NoActiveRoundError

        self.active_round.end()

        for p in self.players:
            result = self.active_round.get_result_for_user(p.user)
            if result is None:
                # user doesn't place a bid at this round
                continue

            if result.is_right_answer:
                p.balance += result.prize

    @property
    def active_round(self) -> Round:
        if self.state in (self.State.BEFORE_ROUNDS, self.State.ALL_ROUNDS_PLAYED):
            raise errors.NoActiveRoundError

        return self.rounds[self._active_round_idx]

    def place_a_bid(self, bid: Bid) -> None:
        player_state = self.get_player_state(bid.user)
        if player_state.balance < bid.amount:
            raise errors.NoEnoughMoneyForBid()

        r = self.active_round
        r.place_a_bid(bid)

        player_state.balance -= bid.amount

    def stop(self):
        if self.started_at is None:
            raise errors.GameNotStartedError

        if self.stopped_at is not None:
            raise errors.GameAlreadyStoppedError

        self.stopped_at = datetime.utcnow()

    def add_player(self, user: User) -> None:
        for p in self.players:
            if p.user.id == user.id:
                raise errors.PlayerAlreadyExistsError

        self.players.append(PlayerState(user=user, balance=self.STARTING_BALANCE))

    def get_player_state(self, user: User) -> PlayerState:
        for p in self.players:
            if p.user.id == user.id:
                return p

        raise errors.PlayerNotFound()

    def add_round(self, wine: Wine) -> None:
        self.rounds.append(
            Round(
                quest_item=QuestItem(wine=wine),
            )
        )
