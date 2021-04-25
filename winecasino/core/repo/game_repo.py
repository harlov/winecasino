from typing import Protocol
from typing import List
from typing import Optional
from uuid import UUID

from winecasino.core.entities import Game


class GameRepo(Protocol):
    async def save(self, game: Game) -> None:
        ...

    async def list(self, game: Game) -> List[Game]:
        ...

    async def fetch(self, pk: UUID) -> Optional[Game]:
        ...
