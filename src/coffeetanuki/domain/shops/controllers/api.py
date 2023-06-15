from typing import Any
from uuid import UUID

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.params import Parameter
from litestar.contrib.repository.filters import CollectionFilter

from pydantic import parse_obj_as

from coffeetanuki.domain.shops.repositories import (
    ShopRepository,
    AmenityRepository,
    provide_shop_repo,
    provide_r_shop_repo,
    provide_amenity_repo,
    provide_r_amenity_repo,
)

from coffeetanuki.domain.shops.schemas import (
    ShopCreate,
    ShopUpdate,
    ShopDB,
    ShopDBFull,
    AmenityCreate,
    AmenityUpdate,
    AmenityDB,
    AmenityDBFull,
)
from coffeetanuki.domain.shops.models import Shop, Amenity
from coffeetanuki.domain.shops.utils import geojsonify


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
    async def list_shops(self, r_shop_repo: ShopRepository) -> list[ShopDBFull]:
        return parse_obj_as(list[ShopDBFull], await r_shop_repo.list())

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
        return geojsonify(parse_obj_as(list[ShopDB], await shop_repo.list()))

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
    ) -> ShopDBFull:
        return parse_obj_as(ShopDBFull, await r_shop_repo.get(shop_id))

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
        data: ShopCreate,
    ) -> ShopDBFull:
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
        obj = await r_shop_repo.add(Shop(**dd))
        await r_shop_repo.session.commit()
        return parse_obj_as(ShopDBFull, obj)

    #
    # @post(
    #     path="/bulk",
    #     operation_id="BulkCreateShop",
    #     name="shops:bulkcreate",
    #     summary="Create multiple new shops.",
    #     tags=["shops"],
    # )
    # async def bulk_create_shop(
    #     self,
    #     r_shop_repo: ShopRepository,
    #     amenity_repo: AmenityRepository,
    #     data: list[ShopCreate],
    # ) -> list[ShopDBFull]:
    #     # create a dict to lookup amenities by name
    #     # avoids amenity table transfer for each new shop
    #     amens = {a.name: a for a in await amenity_repo.list()}
    #     new_shops: list[Shop] = []
    #     for d in data:
    #         dd = d.dict()
    #         dd.update(
    #             {
    #                 "coordinates": f"Point({d.coordinates.lon} {d.coordinates.lat})",
    #                 "amenities": [amens[n] for n in d.amenities],
    #             }
    #         )
    #         new_shops.append(Shop(**dd))
    #     obj = await r_shop_repo.add_many(new_shops)
    #     await r_shop_repo.session.commit()
    #     return parse_obj_as(list[ShopDBFull], obj)

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
        data: ShopUpdate,
        shop_id: UUID = Parameter(
            title="Shop ID",
            description="The shop to update",
        ),
    ) -> ShopDBFull:
        dd = data.dict(exclude_unset=True)
        dd.update({"id": shop_id})
        if "coordinates" in dd and data.coordinates:
            dd["coordinates"] = f"Point({data.coordinates.lon} {data.coordinates.lat})"
        if "amenities" in dd and data.amenities:
            dd["amenities"] = await amenity_repo.list(
                CollectionFilter("name", data.amenities)
            )
        obj = await r_shop_repo.update(Shop(**dd))
        await r_shop_repo.session.commit()
        return parse_obj_as(ShopDBFull, obj)

    # delete shop by id
    @delete(
        path="/{shop_id:uuid}",
        operation_id="DeleteShop",
        name="shops:delete",
        summary="Delete a shop by its ID.",
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
    ) -> list[AmenityDBFull]:
        return parse_obj_as(list[AmenityDBFull], await r_amenity_repo.list())

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
    ) -> AmenityDBFull:
        return parse_obj_as(AmenityDBFull, await r_amenity_repo.get(amenity_id))

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
        data: AmenityCreate,
    ) -> AmenityDB:
        obj = await amenity_repo.add(Amenity(**data.dict()))
        await amenity_repo.session.commit()
        return parse_obj_as(AmenityDB, obj)

    # update amenity
    @patch(
        path="/{amenity_id:uuid}",
        operation_id="UpdateAmenity",
        name="amenities:update",
        summary="Update an amenity by its ID.",
        tags=["amenities"],
    )
    async def update_amenity(
        self,
        amenity_repo: AmenityRepository,
        data: AmenityUpdate,
        amenity_id: UUID = Parameter(
            title="Amenity ID",
            description="The amenity to update",
        ),
    ) -> AmenityDB:
        dd = data.dict(exclude_unset=True)
        dd.update({"id": amenity_id})
        obj = await amenity_repo.update(Amenity(**dd))
        await amenity_repo.session.commit()
        return parse_obj_as(AmenityDB, obj)

    # delete amenity
    @delete(
        path="/{amenity_id:uuid}",
        operation_id="DeleteAmenity",
        name="amenities:delete",
        summary="Delete an amenity by its ID.",
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
