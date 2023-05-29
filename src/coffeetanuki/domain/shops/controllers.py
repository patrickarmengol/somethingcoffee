from typing import Any
from uuid import UUID

from litestar import Controller, get, post
from litestar.contrib.repository.filters import CollectionFilter
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from litestar.di import Provide
from litestar.params import Parameter
from pydantic import parse_obj_as
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from coffeetanuki.domain.shops import models, schemas

__all__ = ["ShopController", "AmenityController"]


class ShopRepository(SQLAlchemyAsyncRepository[models.Shop]):
    """Shop Repository"""

    model_type = models.Shop


async def provide_shop_repo(db_session: AsyncSession) -> ShopRepository:
    return ShopRepository(
        session=db_session,
    )


async def provide_r_shop_repo(db_session: AsyncSession) -> ShopRepository:
    return ShopRepository(
        statement=select(models.Shop).options(selectinload(models.Shop.amenities)),
        session=db_session,
    )


class AmenityRepository(SQLAlchemyAsyncRepository[models.Amenity]):
    """Amenity Repository"""

    model_type = models.Amenity


async def provide_amenity_repo(db_session: AsyncSession) -> AmenityRepository:
    return AmenityRepository(session=db_session)


async def provide_r_amenity_repo(db_session: AsyncSession) -> AmenityRepository:
    return AmenityRepository(
        statement=select(models.Amenity).options(selectinload(models.Amenity.shops)),
        session=db_session,
    )


class ShopController(Controller):
    """Shop CRUD"""

    path = "/api/shops"

    @get(
        path="",
        operation_id="ListShops",
        name="shops:list",
        summary="List all shops.",
        dependencies={"shop_repo": Provide(provide_r_shop_repo)},
    )
    async def list_shops(
        self,
        shop_repo: ShopRepository,
    ) -> list[schemas.ShopReturn]:
        return parse_obj_as(list[schemas.ShopReturn], await shop_repo.list())

    @get(
        path="/geojson",
        operation_id="ListShopsGeoJSON",
        name="shops:listgeojson",
        summary="List all shops in GeoJSON format.",
        dependencies={"shop_repo": Provide(provide_shop_repo)},
    )
    async def list_shops_geojson(
        self,
        shop_repo: ShopRepository,
    ) -> dict[str, Any]:
        shops = parse_obj_as(list[schemas.Shop], await shop_repo.list())
        geojson: dict[str, Any] = {"type": "FeatureCollection", "features": []}
        for shop in shops:
            feature: dict[str, Any] = {
                "type": "Feature",
                "properties": {"name": shop.name},  # perhaps add more attributes here?
                "geometry": {
                    "type": "Point",
                    "coordinates": [shop.coordinates.lon, shop.coordinates.lat],
                },
            }
            geojson["features"].append(feature)
        return geojson

    @get(
        path="/{shop_id:uuid}",
        operation_id="GetShop",
        name="shops:get",
        summary="Get a shop by its ID.",
        dependencies={"shop_repo": Provide(provide_r_shop_repo)},
    )
    async def get_shop(
        self,
        shop_repo: ShopRepository,
        shop_id: UUID = Parameter(
            title="Shop ID",
            description="The shop to retrieve",
        ),
    ) -> schemas.ShopReturn:
        return schemas.ShopReturn.from_orm(await shop_repo.get(shop_id))

    @post(
        path="",
        operation_id="CreateShop",
        name="shops:create",
        summary="Create a new shop.",
        dependencies={
            "shop_repo": Provide(provide_r_shop_repo),
            "amenity_repo": Provide(provide_amenity_repo),
        },
    )
    async def create_shop(
        self,
        shop_repo: ShopRepository,
        amenity_repo: AmenityRepository,
        data: schemas.ShopCreate,
    ) -> schemas.ShopReturn:
        obj = await shop_repo.add(
            models.Shop(
                name=data.name,
                address=data.address,
                coordinates=f"Point({data.coordinates.lon} {data.coordinates.lat})",
                roaster=data.roaster,
                hours_of_operation=data.hours_of_operation,
                amenities=await amenity_repo.list(
                    CollectionFilter("name", [a.name for a in data.amenities])
                ),
            )
        )
        await shop_repo.session.commit()
        return schemas.ShopReturn.from_orm(obj)


class AmenityController(Controller):
    """Amenity CRUD"""

    path = "/api/amenities"

    @get(
        path="",
        operation_id="ListAmenities",
        name="amenities:list",
        summary="List all amenities.",
        dependencies={"amenity_repo": Provide(provide_r_amenity_repo)},
    )
    async def list_amenities(
        self,
        amenity_repo: AmenityRepository,
    ) -> list[schemas.AmenityReturn]:
        return parse_obj_as(list[schemas.AmenityReturn], await amenity_repo.list())

    @post(
        path="",
        operation_id="CreateAmenity",
        name="amenities:create",
        summary="Create a new amenity.",
        dependencies={"amenity_repo": Provide(provide_r_amenity_repo)},
    )
    async def create_amenity(
        self,
        amenity_repo: AmenityRepository,
        data: schemas.AmenityCreate,
    ) -> schemas.AmenityReturn:
        obj = await amenity_repo.add(models.Amenity(**data.dict()))
        await amenity_repo.session.commit()
        return schemas.AmenityReturn.from_orm(obj)
