from __future__ import annotations
from typing import TYPE_CHECKING
from pydantic import BaseModel, UUID4


__all__ = ["TagBase", "TagCreate", "TagUpdate", "TagDB", "TagDBFull"]


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: str | None


class TagDB(TagBase):
    id: UUID4

    class Config:
        orm_mode = True


from coffeetanuki.domain.shops.schemas import ShopDB  # noqa: E402


class TagDBFull(TagDB):
    shops: list[ShopDB]
