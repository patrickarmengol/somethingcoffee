from __future__ import annotations
from typing import TYPE_CHECKING
from litestar.contrib.sqlalchemy.base import UUIDBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from coffeetanuki.domain.shops.models import shop_tag

if TYPE_CHECKING:
    from coffeetanuki.domain.shops.models import Shop

__all__ = ["Tag"]


class Tag(UUIDBase):
    name: Mapped[str] = mapped_column(String(), unique=True)

    shops: Mapped[list[Shop]] = relationship(
        secondary=shop_tag,
        back_populates="tags",
        lazy="selectin",
    )
