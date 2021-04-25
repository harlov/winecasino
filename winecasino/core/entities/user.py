from typing import Optional

from .base import Model


class TelegramAccount(Model):
    login: str
    chat_id: str


class User(Model):
    name: str

    telegram_account: Optional[TelegramAccount]
