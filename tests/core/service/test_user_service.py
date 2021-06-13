import pytest

from winecasino.core import service
from winecasino.core.entities.user import User
from winecasino.core.entities.user import TelegramAccount


pytestmark = pytest.mark.asyncio


async def test_register_user(user_in_memory_repo):
    user = await service.register_user(
        user_repo=user_in_memory_repo,
        telegram_login="user",
        telegram_chat_id="chat_with_user",
    )

    assert user == User(
        id=user.id,
        name="user",
        telegram_account=TelegramAccount(
            id=user.telegram_account.id,
            login="user",
            chat_id="chat_with_user",
        ),
    )
