from copy import deepcopy
from typing import Optional
from uuid import UUID

from winecasino.infra.in_memory_repo.base import BaseInMemoryRepo
from winecasino.core.repo import UserRepo
from winecasino.core.entities.user import User


class UserInMemoryRepo(BaseInMemoryRepo, UserRepo):
    @property
    def users_collection(self):
        return self.get_collection("users")

    async def save(self, user: User) -> None:
        self.users_collection[user.id] = deepcopy(user)

    async def fetch(self, pk: UUID) -> Optional[User]:
        try:
            return deepcopy(self.users_collection[pk])
        except KeyError:
            return None
