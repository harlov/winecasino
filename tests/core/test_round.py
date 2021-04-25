import pytest
from winecasino.core import entities
from winecasino.core.entities import game as game_entities
from winecasino.core.entities import errors

get_fixture = pytest.lazy_fixture


def test_end_round(wine, wine_2, user, user_2, user_3):
    r = game_entities.Round(quest_item=game_entities.QuestItem(wine=wine))

    assert r.is_ended is False

    r.place_a_bid(
        entities.Bid(user=user, amount=100, type=entities.Bid.Type.WINE, b_wine=wine)
    )
    with pytest.raises(errors.RoundIsStillActiveError):
        r.get_result_for_user(user)

    r.place_a_bid(
        entities.Bid(
            user=user_2, amount=100, type=entities.Bid.Type.WINE, b_wine=wine_2
        )
    )

    r.end()

    assert r.is_ended is True
    assert len(r._results) == 2

    with pytest.raises(errors.RoundIsEndedError):
        r.place_a_bid(
            entities.Bid(
                user=user_3, amount=100, type=entities.Bid.Type.WINE, b_wine=wine
            )
        )
    assert len(r._results) == 2

    # Second end should fail
    with pytest.raises(errors.RoundIsEndedError):
        r.end()
    assert len(r._results) == 2

    result_1 = r.get_result_for_user(user)
    assert result_1.is_right_answer is True
    assert result_1.prize == 1100

    result_2 = r.get_result_for_user(user_2)
    assert result_2.is_right_answer is False
    assert result_2.prize == 0

    result_3 = r.get_result_for_user(user_3)
    assert result_3 is None
