from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from coffeetanuki.domain.shops.models import Shop

__all__ = [
    "ShopRepository",
    "provide_shop_repo",
    "provide_r_shop_repo",
]


class ShopRepository(SQLAlchemyAsyncRepository[Shop]):
    """Shop Repository"""

    model_type = Shop


async def provide_shop_repo(db_session: AsyncSession) -> ShopRepository:
    return ShopRepository(
        session=db_session,
    )


async def provide_r_shop_repo(db_session: AsyncSession) -> ShopRepository:
    return ShopRepository(
        statement=select(Shop).options(selectinload(Shop.tags)),
        session=db_session,
    )
