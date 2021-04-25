import pytest

from winecasino.core import entities
from winecasino.core.entities import errors


get_fixture = pytest.lazy_fixture


def test_place_a_bid(
    game_started: entities.Game,
    user: entities.User,
    user_2: entities.User,
    wine: entities.Wine,
    wine_2: entities.Wine,
):
    game_started.start_next_round()
    start_balance = game_started.get_player_state(user).balance
    game_started.place_a_bid(
        entities.Bid(user=user, type=entities.Bid.Type.WINE, b_wine=wine, amount=100)
    )
    balance_after_bid = game_started.get_player_state(user).balance
    assert start_balance - balance_after_bid == 100

    with pytest.raises(errors.PlayerAlreadyPlacedBidError):
        game_started.place_a_bid(
            entities.Bid(
                user=user,
                type=entities.Bid.Type.SUGAR,
                b_sugar=entities.Wine.Sugar.SWEET,
                amount=100,
            )
        )
    assert game_started.get_player_state(user).balance == balance_after_bid

    start_balance_user_2 = game_started.get_player_state(user_2).balance
    game_started.place_a_bid(
        entities.Bid(
            user=user_2, type=entities.Bid.Type.WINE, b_wine=wine_2, amount=200
        )
    )

    assert game_started.get_player_state(user).balance == balance_after_bid
    assert start_balance_user_2 - game_started.get_player_state(user_2).balance == 200


def test_no_enough_money_for_a_bid(
    game_started: entities.Game,
    user: entities.User,
    wine: entities.Wine,
):
    with pytest.raises(errors.NoEnoughMoneyForBid):
        game_started.place_a_bid(
            entities.Bid(
                user=user, type=entities.Bid.Type.WINE, b_wine=wine, amount=1001
            )
        )


@pytest.mark.parametrize(
    "wine_fixture, matched_expected",
    [
        (get_fixture("wine_sweet"), True),
        (get_fixture("wine_semi_sweet"), False),
        (get_fixture("wine_semi_dry"), False),
        (get_fixture("wine_dry"), False),
    ],
)
def test_bid_matched_sugar(user, wine_fixture, matched_expected):
    bid = entities.Bid(
        user=user,
        type=entities.Bid.Type.SUGAR,
        b_sugar=entities.Wine.Sugar.SWEET,
        amount=100,
    )

    assert bid.is_matched(wine_fixture) is matched_expected


@pytest.mark.parametrize(
    "wine_fixture, matched_expected",
    [
        (get_fixture("wine_country_old"), True),
        (get_fixture("wine_country_new"), False),
        (get_fixture("wine_country_ex_ussr"), False),
    ],
)
def test_bid_matched_part_of_world(user, wine_fixture, matched_expected):
    bid = entities.Bid(
        user=user,
        type=entities.Bid.Type.PART_OF_WORLD,
        b_part_of_world=entities.Country.PartOfWorld.OLD_WORLD,
        amount=100,
    )

    assert bid.is_matched(wine_fixture) is matched_expected


@pytest.mark.parametrize(
    "wine_fixture, matched_expected",
    [
        (get_fixture("wine_country_old"), True),
        (get_fixture("wine_country_new"), False),
        (get_fixture("wine_country_ex_ussr"), False),
    ],
)
def test_bid_matched_country(user, country_old, wine_fixture, matched_expected):
    bid = entities.Bid(
        user=user,
        type=entities.Bid.Type.COUNTRY,
        b_country=country_old,
        amount=100,
    )

    assert bid.is_matched(wine_fixture) is matched_expected


@pytest.mark.parametrize(
    "wine_fixture, matched_expected",
    [
        (get_fixture("wine"), True),
        (get_fixture("wine_2"), False),
    ],
)
def test_bid_matched_wine(user, wine, wine_fixture, matched_expected):
    bid = entities.Bid(
        user=user,
        type=entities.Bid.Type.WINE,
        b_wine=wine,
        amount=100,
    )

    assert bid.is_matched(wine_fixture) is matched_expected
