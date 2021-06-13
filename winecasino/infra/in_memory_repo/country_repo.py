from copy import deepcopy
from typing import Optional
from uuid import UUID

from winecasino.infra.in_memory_repo.base import BaseInMemoryRepo
from winecasino.core.repo import CountryRepo
from winecasino.core.entities.country import Country


class CountryInMemoryRepo(BaseInMemoryRepo, CountryRepo):
    @property
    def countries_collection(self):
        return self.get_collection("countries")

    async def save(self, country: Country) -> None:
        self.countries_collection[country.id] = deepcopy(country)

    async def fetch(self, pk: UUID) -> Optional[Country]:
        try:
            return deepcopy(self.countries_collection[pk])
        except KeyError:
            return None
