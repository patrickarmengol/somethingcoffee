from typing import Any
from uuid import UUID
from geoalchemy2 import WKTElement

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.params import Parameter
from litestar.contrib.repository.filters import CollectionFilter
from sqlalchemy import select, func

from pydantic import parse_obj_as
from sqlalchemy.ext.asyncio import AsyncSession

from coffeetanuki.domain.shops.dependencies import (
    ShopRepository,
    provide_shop_repo,
    provide_r_shop_repo,
)

from coffeetanuki.domain.tags.dependencies import (
    TagRepository,
    provide_tag_repo,
)

from coffeetanuki.domain.shops.schemas import ShopCreate, ShopUpdate, ShopDB, ShopDBFull
from coffeetanuki.domain.shops.models import Shop

from coffeetanuki.domain.shops.utils import geojsonify


class ShopAPIController(Controller):
    """Shop CRUD"""

    path = "/api/shops"
    dependencies = {
        "shop_repo": Provide(provide_shop_repo),
        "r_shop_repo": Provide(provide_r_shop_repo),
        "tag_repo": Provide(provide_tag_repo),
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

    # list shops within distance of central point
    @get(
        path="/dwithin",
        operation_id="ListShopsDwithin",
        name="shops:listdwithin",
        summary="List all shops within a radius distance from a central point.",
        tags=["shops"],
    )
    async def list_shops_dwithin(
        self,
        db_session: AsyncSession,
        lon: float = Parameter(
            title="centroid-lon",
            description="Longitude coordinate of centroid.",
        ),
        lat: float = Parameter(
            title="centroid-lat",
            description="Latitude coordinate of centroid.",
        ),
        radius: float = Parameter(
            title="radius",
            description="The radius distance in meters around the centroid to include.",
        ),
    ) -> list[ShopDBFull]:
        point = WKTElement(f"Point({lon} {lat})")
        query = select(Shop).where(func.ST_Dwithin(Shop.coordinates, point, radius))

        instances = list((await db_session.execute(query)).scalars())
        for instance in instances:
            db_session.expunge(instance)

        return parse_obj_as(list[ShopDBFull], instances)

    # list intersect with bbox
    @get(
        path="/bbox",
        operation_id="ListShopsInBbox",
        name="shops:listbbox",
        summary="List shops that inside a bounding box.",
        tags=["shops"],
    )
    async def list_shops_bbox(
        self,
        db_session: AsyncSession,
        in_bbox: str = Parameter(
            title="bbox",
            description="Number of nearest neighbors to include.",
        ),
    ) -> list[ShopDBFull]:
        try:
            p1x, p1y, p2x, p2y = (int(n) for n in in_bbox.split(","))
        except ValueError:
            raise ValueError(f"Invalid bbox string supplied for parameter {in_bbox}")

        bbox = WKTElement(
            f"POLYGON(({p1x} {p1y},{p1x} {p2y},{p2x} {p2y},{p2x} {p1y},{p1x} {p1y}))",
            srid=4326,
        )
        query = select(Shop).where(Shop.coordinates.intersects(bbox))

        instances = list((await db_session.execute(query)).scalars())
        for instance in instances:
            db_session.expunge(instance)

        return parse_obj_as(list[ShopDBFull], instances)

    # list k-nearest-neighbors of central point
    @get(
        path="/knn",
        operation_id="ListShopsKNN",
        name="shops:listknn",
        summary="List k-nearest-neighbor shops from a central point.",
        tags=["shops"],
    )
    async def list_shops_knn(
        self,
        db_session: AsyncSession,
        lon: float = Parameter(
            title="centroid-lon",
            description="Longitude coordinate of centroid.",
        ),
        lat: float = Parameter(
            title="centroid-lat",
            description="Latitude coordinate of centroid.",
        ),
        k: int = Parameter(
            title="k", description="Number of nearest neighbors to include."
        ),
    ) -> list[ShopDBFull]:
        point = WKTElement(f"Point({lon} {lat})", srid=4326)
        query = (
            select(Shop).order_by(Shop.coordinates.distance_centroid(point)).limit(k)
        )

        instances = list((await db_session.execute(query)).scalars())
        for instance in instances:
            db_session.expunge(instance)

        return parse_obj_as(list[ShopDBFull], instances)

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
        tag_repo: TagRepository,
        data: ShopCreate,
    ) -> ShopDBFull:
        dd = data.dict()
        dd.update(
            {
                "coordinates": f"Point({data.coordinates.lon} {data.coordinates.lat})",
                "tags": await tag_repo.list(CollectionFilter("name", data.tag_names))
                if data.tag_names
                else [],
            }
        )
        del dd["tag_names"]
        obj = await r_shop_repo.add(Shop(**dd))
        await r_shop_repo.session.commit()
        return parse_obj_as(ShopDBFull, obj)

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
        tag_repo: TagRepository,
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
        if "tag_names" in dd and data.tag_names:
            dd["tags"] = await tag_repo.list(CollectionFilter("name", data.tag_names))
            del dd["tag_names"]
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
