import pytest

from winecasino.core import entities

# Countries
@pytest.fixture
def country_old():
    return entities.Country(
        id=entities.new_id(),
        name="France",
        part_of_world=entities.Country.PartOfWorld.OLD_WORLD,
    )


@pytest.fixture
def country_new():
    return entities.Country(
        id=entities.new_id(),
        name="Chili",
        part_of_world=entities.Country.PartOfWorld.NEW_WORLD,
    )


@pytest.fixture
def country_ex_ussr():
    return entities.Country(
        id=entities.new_id(),
        name="Georgia",
        part_of_world=entities.Country.PartOfWorld.EX_USSR,
    )


# Grapes
@pytest.fixture
def grape():
    return entities.Grape(id=entities.new_id(), name="Grape")


@pytest.fixture
def grape_2():
    return entities.Grape(id=entities.new_id(), name="Grape 2")


# Users
@pytest.fixture
def user():
    return entities.User(id=entities.new_id(), name="user")


@pytest.fixture
def user_2():
    return entities.User(id=entities.new_id(), name="user_2")


@pytest.fixture
def user_3():
    return entities.User(id=entities.new_id(), name="user_3")


# Wines
@pytest.fixture
def wine(country_old, grape):
    return entities.Wine(
        id=entities.new_id(),
        name="Wine",
        color=entities.Wine.Color.RED,
        sugar=entities.Wine.Sugar.SWEET,
        country=country_old,
        grape=grape,
    )


@pytest.fixture
def wine_2(country_new, grape_2):
    return entities.Wine(
        id=entities.new_id(),
        name="Wine 2",
        color=entities.Wine.Color.RED,
        sugar=entities.Wine.Sugar.SWEET,
        country=country_new,
        grape=grape_2,
    )


@pytest.fixture
def wine_sweet(country_old, grape):
    return entities.Wine(
        id=entities.new_id(),
        name="Wine Sweet",
        color=entities.Wine.Color.RED,
        sugar=entities.Wine.Sugar.SWEET,
        country=country_old,
        grape=grape,
    )


@pytest.fixture
def wine_semi_sweet(country_old, grape):
    return entities.Wine(
        id=entities.new_id(),
        name="Wine Semi Sweet",
        color=entities.Wine.Color.RED,
        sugar=entities.Wine.Sugar.SEMI_SWEET,
        country=country_old,
        grape=grape,
    )


@pytest.fixture
def wine_semi_dry(country_old, grape):
    return entities.Wine(
        id=entities.new_id(),
        name="Wine Semi Dry",
        color=entities.Wine.Color.RED,
        sugar=entities.Wine.Sugar.SEMI_DRY,
        country=country_old,
        grape=grape,
    )


@pytest.fixture
def wine_dry(country_old, grape):
    return entities.Wine(
        id=entities.new_id(),
        name="Wine Dry",
        color=entities.Wine.Color.RED,
        sugar=entities.Wine.Sugar.DRY,
        country=country_old,
        grape=grape,
    )


@pytest.fixture
def wine_country_old(country_old, grape):
    return entities.Wine(
        id=entities.new_id(),
        name="Wine Country Old",
        color=entities.Wine.Color.RED,
        sugar=entities.Wine.Sugar.DRY,
        country=country_old,
        grape=grape,
    )


@pytest.fixture
def wine_country_new(country_new, grape):
    return entities.Wine(
        id=entities.new_id(),
        name="Wine Country New",
        color=entities.Wine.Color.RED,
        sugar=entities.Wine.Sugar.DRY,
        country=country_new,
        grape=grape,
    )


@pytest.fixture
def wine_country_ex_ussr(country_ex_ussr, grape):
    return entities.Wine(
        id=entities.new_id(),
        name="Wine Country Ex Ussr",
        color=entities.Wine.Color.RED,
        sugar=entities.Wine.Sugar.DRY,
        country=country_ex_ussr,
        grape=grape,
    )


# Games
@pytest.fixture
def game_without_players():
    return entities.Game(id=entities.new_id(), name="Game")


@pytest.fixture
def game_with_one_player(user):
    g = entities.Game(id=entities.new_id(), name="Game")
    g.add_player(user)
    return g


@pytest.fixture
def game_without_rounds(user, user_2):
    g = entities.Game(id=entities.new_id(), name="Game")
    g.add_player(user)
    g.add_player(user_2)
    return g


@pytest.fixture
def game_with_one_round(user, user_2, wine):
    g = entities.Game(id=entities.new_id(), name="Game")
    g.add_player(user)
    g.add_player(user_2)
    g.add_round(wine)
    return g


@pytest.fixture
def game(user, user_2, wine, wine_2):
    g = entities.Game(id=entities.new_id(), name="Game")
    g.add_player(user)
    g.add_player(user_2)

    g.add_round(wine)
    g.add_round(wine_2)

    return g


@pytest.fixture
def game_started(user, user_2, wine, wine_2):
    g = entities.Game(id=entities.new_id(), name="Game")
    g.add_player(user)
    g.add_player(user_2)

    g.add_round(wine)
    g.add_round(wine_2)

    g.start()

    return g
