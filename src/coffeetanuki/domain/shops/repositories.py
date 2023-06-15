from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from coffeetanuki.domain.shops.models import Shop, Amenity

__all__ = [
    "ShopRepository",
    "provide_shop_repo",
    "provide_r_shop_repo",
    "AmenityRepository",
    "provide_amenity_repo",
    "provide_r_amenity_repo",
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
        statement=select(Shop).options(selectinload(Shop.amenities)),
        session=db_session,
    )


class AmenityRepository(SQLAlchemyAsyncRepository[Amenity]):
    """Amenity Repository"""

    model_type = Amenity


async def provide_amenity_repo(db_session: AsyncSession) -> AmenityRepository:
    return AmenityRepository(session=db_session)


async def provide_r_amenity_repo(db_session: AsyncSession) -> AmenityRepository:
    return AmenityRepository(
        statement=select(Amenity).options(selectinload(Amenity.shops)),
        session=db_session,
    )
