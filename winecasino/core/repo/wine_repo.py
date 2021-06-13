from typing import Protocol
from typing import List
from typing import Optional
from uuid import UUID

from winecasino.core.entities import Wine


class WineRepo(Protocol):
    async def save(self, wine: Wine) -> None:
        ...

    async def list(self, game: Wine) -> List[Wine]:
        ...

    async def fetch(self, pk: UUID) -> Optional[Wine]:
        ...
