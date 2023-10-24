from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from somethingcoffee.domain.shops.models import Shop
from typing import Any

__all__ = [
    "ShopRepository",
    "provide_shop_repo",
]


class ShopRepository(SQLAlchemyAsyncRepository[Shop]):
    """Shop Repository"""

    model_type = Shop


async def provide_shop_repo(db_session: AsyncSession) -> ShopRepository:
    return ShopRepository(
        statement=select(Shop),
        session=db_session,
    )
