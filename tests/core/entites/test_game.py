import pytest
from winecasino.core import entities
from winecasino.core.entities import errors

from winecasino.core.entities.game import PlayerState

get_fixture = pytest.lazy_fixture


def test_add_player_into_game(user, user_2, user_3):
    g = entities.Game(id=entities.new_id(), name="First game")

    g.add_player(user)
    assert g.get_player_state(user) == PlayerState(
        user=user, balance=entities.Game.STARTING_BALANCE
    )

    g.add_player(user_2)
    assert g.get_player_state(user_2) == PlayerState(
        user=user_2, balance=entities.Game.STARTING_BALANCE
    )

    assert g.players == [
        PlayerState(user=user, balance=entities.Game.STARTING_BALANCE),
        PlayerState(user=user_2, balance=entities.Game.STARTING_BALANCE),
    ]

    with pytest.raises(errors.PlayerAlreadyExistsError):
        g.add_player(user)

    with pytest.raises(errors.PlayerNotFound):
        assert g.get_player_state(user_3) is None


@pytest.mark.parametrize(
    "game_fixture",
    [
        get_fixture("game_without_players"),
        get_fixture("game_with_one_player"),
    ],
)
def test_start_game_no_enough_players(game_fixture: entities.Game):
    with pytest.raises(errors.NoEnoughPlayersInTheGameError):
        game_fixture.start()
    assert game_fixture.started_at is None


@pytest.mark.parametrize(
    "game_fixture",
    [
        get_fixture("game_without_rounds"),
        get_fixture("game_with_one_round"),
    ],
)
def test_start_game_no_enough_rounds(game_fixture: entities.Game):
    with pytest.raises(errors.NoEnoughRoundsInTheGameError):
        game_fixture.start()
    assert game_fixture.started_at is None


def test_start_game(game: entities.Game):
    game.start()
    assert game.started_at is not None
    assert game.stopped_at is None
    with pytest.raises(errors.NoActiveRoundError):
        game.active_round


def test_start_next_round(game_started: entities.Game):
    assert game_started.start_next_round() is True
    game_started.finish_current_round()

    assert game_started.start_next_round() is True
    game_started.finish_current_round()

    assert game_started.start_next_round() is False  # Game only have two rounds
    assert (
        game_started.start_next_round() is False
    )  # All next calls should be False too.

    with pytest.raises(errors.NoActiveRoundError):
        game_started.finish_current_round()


def test_finish_round_balance(
    game_started: entities.Game,
    user: entities.User,
    user_2: entities.User,
    wine: entities.Wine,
    wine_2: entities.Wine,
):
    game_started.start_next_round()
    game_started.place_a_bid(
        entities.Bid(
            user=user,
            type=entities.Bid.Type.WINE,
            b_wine=wine,
            amount=100,
        )
    )
    game_started.place_a_bid(
        entities.Bid(
            user=user_2,
            type=entities.Bid.Type.WINE,
            b_wine=wine_2,
            amount=100,
        )
    )
    game_started.finish_current_round()
    assert game_started.get_player_state(user).balance == 2000
    assert game_started.get_player_state(user_2).balance == 900


def test_start_game_twice(game_started: entities.Game):
    started_at = game_started.started_at
    with pytest.raises(errors.GameAlreadyStartedError):
        game_started.start()

    assert game_started.started_at == started_at


def test_stop_game(game_started: entities.Game):
    game_started.stop()
    assert game_started.stopped_at is not None
    stopped_at = game_started.stopped_at

    with pytest.raises(errors.GameAlreadyStoppedError):
        game_started.stop()

    assert game_started.stopped_at == stopped_at


def test_stop_game_not_started(game: entities.Game):
    with pytest.raises(errors.GameNotStartedError):
        game.stop()

    assert game.stopped_at is None
