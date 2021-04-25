from typing import Protocol
from typing import Optional
from uuid import UUID

from winecasino.core.entities import User


class UserRepo(Protocol):
    async def save(self, user: User) -> None:
        ...

    async def fetch(self, pk: UUID) -> Optional[User]:
        ...
