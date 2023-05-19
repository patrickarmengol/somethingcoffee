from geoalchemy2 import Geography
from litestar.contrib.sqlalchemy.base import UUIDBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


__all__ = ["Shop"]


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
