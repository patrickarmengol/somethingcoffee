from __future__ import annotations
from pydantic import BaseModel, UUID4


__all__ = ["TagBase", "TagCreate", "TagUpdate", "TagDB", "TagDBFull"]


class TagBase(BaseModel):
    scope: str  # what kind of tag; e.g. amenity, offering
    name: str  # what the tag represents; e.g. wifi, oatmilk


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    scope: str | None
    name: str | None


class TagDB(TagBase):
    id: UUID4

    class Config:
        orm_mode = True


from coffeetanuki.domain.shops.schemas import ShopDB  # noqa: E402


class TagDBFull(TagDB):
    shops: list[ShopDB]
