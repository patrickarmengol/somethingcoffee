from __future__ import annotations
from geoalchemy2 import Geography
from litestar.contrib.sqlalchemy.base import UUIDBase
from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship


__all__ = ["Shop", "Amenity", "shop_amenity"]


shop_amenity = Table(
    "shop_amenity",
    UUIDBase.metadata,
    Column("shop_id", ForeignKey("shop.id")),
    Column("amenity_id", ForeignKey("amenity.id")),
)


class Amenity(UUIDBase):
    name: Mapped[str] = mapped_column(String(), unique=True)

    shops: Mapped[list[Shop]] = relationship(
        secondary=shop_amenity,
        back_populates="amenities",
        lazy="selectin",
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

    amenities: Mapped[list[Amenity]] = relationship(
        secondary=shop_amenity,
        back_populates="shops",
        lazy="selectin",
    )
