from pydantic import BaseModel, UUID4

from coffeetanuki.domain.shops.schemas import ShopDB

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


class TagDBFull(TagDB):
    shops: list[ShopDB]
