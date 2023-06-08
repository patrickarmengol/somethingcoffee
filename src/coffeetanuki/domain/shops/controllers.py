from typing import Any
from uuid import UUID

from litestar import Controller, delete, get, patch, post
from litestar.contrib.repository.filters import CollectionFilter
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from litestar.di import Provide
from litestar.params import Parameter
from litestar.response_containers import Template
from pydantic import parse_obj_as
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from coffeetanuki.domain.shops import models, schemas

__all__ = ["ShopAPIController", "AmenityAPIController", "ShopWebController"]


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


class ShopAPIController(Controller):
    """Shop CRUD"""

    path = "/api/shops"
    dependencies = {
        "shop_repo": Provide(provide_shop_repo),
        "r_shop_repo": Provide(provide_r_shop_repo),
        "amenity_repo": Provide(provide_amenity_repo),
        "r_amenity_repo": Provide(provide_r_amenity_repo),
    }

    # list shops
    @get(
        path="",
        operation_id="ListShops",
        name="shops:list",
        summary="List all shops.",
        tags=["shops"],
    )
    async def list_shops(
        self,
        r_shop_repo: ShopRepository,
    ) -> list[schemas.ShopDBFull]:
        return parse_obj_as(list[schemas.ShopDBFull], await r_shop_repo.list())

    # list shops - geojson
    @get(
        path="/geojson",
        operation_id="ListShopsGeoJSON",
        name="shops:listgeojson",
        summary="List all shops in GeoJSON format.",
        tags=["shops"],
    )
    async def list_shops_geojson(
        self,
        shop_repo: ShopRepository,
    ) -> dict[str, Any]:
        shops = parse_obj_as(list[schemas.ShopDB], await shop_repo.list())
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

    # get shop by id
    @get(
        path="/{shop_id:uuid}",
        operation_id="GetShop",
        name="shops:get",
        summary="Get a shop by its ID.",
        tags=["shops"],
    )
    async def get_shop(
        self,
        r_shop_repo: ShopRepository,
        shop_id: UUID = Parameter(
            title="Shop ID",
            description="The shop to retrieve",
        ),
    ) -> schemas.ShopDBFull:
        return schemas.ShopDBFull.from_orm(await r_shop_repo.get(shop_id))

    # create shop
    @post(
        path="",
        operation_id="CreateShop",
        name="shops:create",
        summary="Create a new shop.",
        tags=["shops"],
    )
    async def create_shop(
        self,
        r_shop_repo: ShopRepository,
        amenity_repo: AmenityRepository,
        data: schemas.ShopCreate,
    ) -> schemas.ShopDBFull:
        dd = data.dict()
        dd.update(
            {
                "coordinates": f"Point({data.coordinates.lon} {data.coordinates.lat})",
                "amenities": await amenity_repo.list(
                    CollectionFilter("name", data.amenities)
                )
                if data.amenities
                else [],
            }
        )
        obj = await r_shop_repo.add(models.Shop(**dd))
        await r_shop_repo.session.commit()
        return schemas.ShopDBFull.from_orm(obj)

    # update shop by id
    @patch(
        path="/{shop_id:uuid}",
        operation_id="UpdateShop",
        name="shops:update",
        summary="Update a shop by its ID.",
        tags=["shops"],
    )
    async def update_shop(
        self,
        r_shop_repo: ShopRepository,
        amenity_repo: AmenityRepository,
        data: schemas.ShopUpdate,
        shop_id: UUID = Parameter(
            title="Shop ID",
            description="The shop to update",
        ),
    ) -> schemas.ShopDBFull:
        dd = data.dict(exclude_unset=True)
        dd.update({"id": shop_id})
        if "coordinates" in dd and data.coordinates:
            dd["coordinates"] = f"Point({data.coordinates.lon} {data.coordinates.lat})"
        if "amenities" in dd and data.amenities:
            dd["amenities"] = await amenity_repo.list(
                CollectionFilter("name", data.amenities)
            )
        obj = await r_shop_repo.update(models.Shop(**dd))
        await r_shop_repo.session.commit()
        return schemas.ShopDBFull.from_orm(obj)

    # delete shop by id
    @delete(
        path="/{shop_id:uuid}",
        operation_id="DeleteShop",
        name="shops:delete",
        summary="Delete a shop by its ID",
        tags=["shops"],
    )
    async def delete_shop(
        self,
        r_shop_repo: ShopRepository,
        shop_id: UUID = Parameter(
            title="Shop ID",
            description="The shop to delete",
        ),
    ) -> None:
        _ = await r_shop_repo.delete(shop_id)
        await r_shop_repo.session.commit()


class AmenityAPIController(Controller):
    """Amenity CRUD"""

    path = "/api/amenities"
    dependencies = {
        "amenity_repo": Provide(provide_amenity_repo),
        "r_amenity_repo": Provide(provide_r_amenity_repo),
    }

    # list amenities
    @get(
        path="",
        operation_id="ListAmenities",
        name="amenities:list",
        summary="List all amenities.",
        tags=["amenities"],
    )
    async def list_amenities(
        self,
        r_amenity_repo: AmenityRepository,
    ) -> list[schemas.AmenityDBFull]:
        return parse_obj_as(list[schemas.AmenityDBFull], await r_amenity_repo.list())

    # get amenity by id
    @get(
        path="/{amenity_id:uuid}",
        operation_id="GetAmenity",
        name="amenities:get",
        summary="Get an amenity by its ID.",
        tags=["amenities"],
    )
    async def get_amenity(
        self,
        r_amenity_repo: AmenityRepository,
        amenity_id: UUID = Parameter(
            title="Amenity ID",
            description="Amenity to retrieve",
        ),
    ) -> schemas.AmenityDBFull:
        return schemas.AmenityDBFull.from_orm(await r_amenity_repo.get(amenity_id))

    # create amenity
    @post(
        path="",
        operation_id="CreateAmenity",
        name="amenities:create",
        summary="Create a new amenity.",
        tags=["amenities"],
    )
    async def create_amenity(
        self,
        amenity_repo: AmenityRepository,
        data: schemas.AmenityCreate,
    ) -> schemas.AmenityDB:
        obj = await amenity_repo.add(models.Amenity(**data.dict()))
        await amenity_repo.session.commit()
        return schemas.AmenityDB.from_orm(obj)

    # update amenity
    @patch(
        path="/{amenity_id:uuid}",
        operation_id="UpdateAmenity",
        name="amenities:update",
        summary="Update an amenity by its ID",
        tags=["amenities"],
    )
    async def update_amenity(
        self,
        amenity_repo: AmenityRepository,
        data: schemas.AmenityUpdate,
        amenity_id: UUID = Parameter(
            title="Amenity ID",
            description="The amenity to update",
        ),
    ) -> schemas.AmenityDB:
        dd = data.dict(exclude_unset=True)
        dd.update({"id": amenity_id})
        obj = await amenity_repo.update(models.Amenity(**dd))
        await amenity_repo.session.commit()
        return schemas.AmenityDB.from_orm(obj)

    # delete amenity
    @delete(
        path="/{amenity_id:uuid}",
        operation_id="DeleteAmenity",
        name="amenities:delete",
        summary="Delete an amenity by its ID",
        tags=["amenities"],
    )
    async def delete_amenity(
        self,
        r_amenity_repo: AmenityRepository,
        amenity_id: UUID = Parameter(
            title="Amenity ID",
            description="The amenity to delete",
        ),
    ) -> None:
        _ = await r_amenity_repo.delete(amenity_id)
        await r_amenity_repo.session.commit()


class ShopWebController(Controller):
    """Shop webpage rendering"""

    path = "/shops"
    dependencies = {
        "shop_repo": Provide(provide_shop_repo),
        "r_shop_repo": Provide(provide_r_shop_repo),
    }

    @get(path="", include_in_schema=False)
    async def shop_list_page(
        self,
        r_shop_repo: ShopRepository,
    ) -> Template:
        shops = parse_obj_as(list[schemas.ShopDBFull], await r_shop_repo.list())
        return Template("views/shop-list.html.jinja", context={"shops": shops})

    @get(path="/{shop_id:uuid}", include_in_schema=False)
    async def shop_details_page(
        self,
        r_shop_repo: ShopRepository,
        shop_id: UUID = Parameter(
            title="Shop ID",
            description="The shop to retrieve",
        ),
    ) -> Template:
        shop = schemas.ShopDBFull.from_orm(await r_shop_repo.get(shop_id))
        return Template("views/shop-details.html.jinja", context={"shop": shop})
