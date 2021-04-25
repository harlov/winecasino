from typing import Any
from uuid import UUID


class BaseInMemoryRepo:
    _store: dict[str, dict[UUID, Any]]

    def __init__(self, init_store: dict[str, dict[UUID, Any]]):
        self._store = init_store

    def get_collection(self, name: str) -> dict[UUID, Any]:
        return self._store[name]
