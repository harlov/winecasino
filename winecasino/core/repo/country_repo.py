from typing import Protocol
from typing import List
from typing import Optional
from uuid import UUID

from winecasino.core.entities import Country


class CountryRepo(Protocol):
    async def save(self, country: Country) -> None:
        ...

    async def list(self, country: Country) -> List[Country]:
        ...

    async def fetch(self, pk: UUID) -> Optional[Country]:
        ...
