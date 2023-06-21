from __future__ import annotations
from geoalchemy2 import Geography
from litestar.contrib.sqlalchemy.base import UUIDBase
from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from coffeetanuki.domain.tags.models import Tag


__all__ = ["Shop", "shop_tag"]


shop_tag = Table(
    "shop_tag",
    UUIDBase.metadata,
    Column("shop_id", ForeignKey("shop.id")),
    Column("tag_id", ForeignKey("tag.id")),
)


class Shop(UUIDBase):
    name: Mapped[str] = mapped_column(String(), unique=True)
    address: Mapped[str]
    coordinates: Mapped[Geography] = mapped_column(
        Geography(
            geometry_type="POINT",
            srid=4326,
            nullable=False,
            # spatial_index=True,
        )
    )
    roaster: Mapped[str | None]
    hours_of_operation: Mapped[str | None]
    description: Mapped[str | None]

    tags: Mapped[list[Tag]] = relationship(
        secondary=shop_tag,
        back_populates="shops",
        lazy="selectin",
    )
