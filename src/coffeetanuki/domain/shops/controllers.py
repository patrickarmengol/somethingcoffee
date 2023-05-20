from typing import Any
from uuid import UUID

from litestar import Controller, get, post
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from litestar.di import Provide
from litestar.params import Parameter
from pydantic import parse_obj_as
from sqlalchemy.ext.asyncio import AsyncSession

from coffeetanuki.domain.shops import models, schemas

__all__ = ["ShopRepository", "provide_shop_repo", "ShopController"]


class ShopRepository(SQLAlchemyAsyncRepository[models.Shop]):
    """Shop Repository"""

    model_type = models.Shop


async def provide_shop_repo(db_session: AsyncSession) -> ShopRepository:
    return ShopRepository(session=db_session)


class ShopController(Controller):
    """Shop CRUD"""

    path = "/api/shops"
    dependencies = {"shop_repo": Provide(provide_shop_repo)}

    @get(
        path="",
        operation_id="ListShops",
        name="shops:list",
        summary="List all shops.",
    )
    async def list_shops(
        self,
        shop_repo: ShopRepository,
    ) -> list[schemas.Shop]:
        return parse_obj_as(list[schemas.Shop], await shop_repo.list())

    @get(
        path="/geojson",
        operation_id="ListShopsGeoJSON",
        name="shops:listgeojson",
        summary="List all shops in GeoJSON format.",
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
                "properties": {"name": shop.name},
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
    )
    async def get_shop(
        self,
        shop_repo: ShopRepository,
        shop_id: UUID = Parameter(
            title="Shop ID",
            description="The shop to retrieve",
        ),
    ) -> schemas.Shop:
        return schemas.Shop.from_orm(await shop_repo.get(shop_id))

    @post(
        path="",
        operation_id="CreateShop",
        name="shops:create",
        summary="Create a new shop.",
    )
    async def create_shop(
        self,
        shop_repo: ShopRepository,
        data: schemas.ShopCreate,
    ) -> schemas.Shop:
        obj = await shop_repo.add(
            models.Shop(
                name=data.name,
                address=data.address,
                coordinates=f"Point({data.coordinates.lon} {data.coordinates.lat})",
                roaster=data.roaster,
                hours_of_operation=data.hours_of_operation,
            )
        )
        await shop_repo.session.commit()
        return schemas.Shop.from_orm(obj)
