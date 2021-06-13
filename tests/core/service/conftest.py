import pytest

from winecasino.infra.in_memory_repo import UserInMemoryRepo
from winecasino.infra.in_memory_repo import CountryInMemoryRepo
from winecasino.core import entities


@pytest.fixture
def in_memory_store():
    return {"users": {}, "countries": {}}


@pytest.fixture
def user_in_memory_repo(in_memory_store):
    return UserInMemoryRepo(init_store=in_memory_store)


@pytest.fixture
def country_in_memory_repo(in_memory_store):
    return CountryInMemoryRepo(init_store=in_memory_store)


@pytest.fixture
async def user(user_in_memory_repo):
    user = entities.User(
        id=entities.new_id(),
        name="user",
        telegram_account=entities.TelegramAccount(
            id=entities.new_id(),
            login="user",
            chat_id="chat_with_user",
        ),
    )
    await user_in_memory_repo.save(user)
    return user
