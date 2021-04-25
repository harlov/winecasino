import uuid

from pydantic import BaseModel
from pydantic import Field
from pydantic import PrivateAttr

ValueObject = BaseModel


class Model(BaseModel):
    id: uuid.UUID

    class Config:
        orm_mode = True
        allow_mutation = True


def new_id() -> uuid.UUID:
    return uuid.uuid4()


__all__ = [
    "Model",
    "Field",
    "ValueObject",
    "PrivateAttr",
    "new_id",
]
