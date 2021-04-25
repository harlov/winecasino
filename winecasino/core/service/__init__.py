from winecasino.core import entities
from winecasino.core import repo


async def register_user(
    user_repo: repo.UserRepo, telegram_login: str, telegram_chat_id: str
) -> entities.User:
    user = entities.User(
        id=entities.new_id(),
        name=telegram_login,
        telegram_account=entities.TelegramAccount(
            id=entities.new_id(), login=telegram_login, chat_id=telegram_chat_id
        ),
    )
    await user_repo.save(user)
    return user