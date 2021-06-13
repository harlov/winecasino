import pytest

from winecasino.core import service
from winecasino.core.entities import Country


pytestmark = pytest.mark.asyncio



async def test_create_country(country_in_memory_repo):
    country = await service.create_country(
        country_repo=country_in_memory_repo,
        name="Russia",

    )

    assert country == Country(
        id=country.id,
        name=country.name,

    )