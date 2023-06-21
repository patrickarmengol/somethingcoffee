from litestar.contrib.sqlalchemy.base import UUIDBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from coffeetanuki.domain.shops.models import Shop, shop_tag

__all__ = ["Tag"]


class Tag(UUIDBase):
    name: Mapped[str] = mapped_column(String(), unique=True)

    shops: Mapped[list[Shop]] = relationship(
        secondary=shop_tag,
        back_populates="tags",
        lazy="selectin",
    )
