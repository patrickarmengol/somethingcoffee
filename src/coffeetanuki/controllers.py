from uuid import UUID
from typing import Any
from litestar import Controller, get, post
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from litestar.di import Provide
from litestar.params import Parameter
from sqlalchemy.ext.asyncio import AsyncSession
from coffeetanuki import models, schemas
from pydantic import parse_obj_as
from litestar.response_containers import Template


class ShopRepository(SQLAlchemyAsyncRepository[models.Shop]):
    """Shop Repository"""

    model_type = models.Shop


async def provide_shop_repo(db_session: AsyncSession) -> ShopRepository:
    return ShopRepository(session=db_session)


class ShopController(Controller):
    """Shop CRUD"""

    path = "/shops"
    dependencies = {"shop_repo": Provide(provide_shop_repo)}

    @get()
    async def list_shops(
        self,
        shop_repo: ShopRepository,
    ) -> list[schemas.Shop]:
        return parse_obj_as(list[schemas.Shop], await shop_repo.list())

    @get("/geojson")
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

    @get("/{shop_id:uuid}")
    async def get_shop(
        self,
        shop_repo: ShopRepository,
        shop_id: UUID = Parameter(
            title="Shop ID",
            description="The shop to retrieve",
        ),
    ) -> schemas.Shop:
        return schemas.Shop.from_orm(await shop_repo.get(shop_id))

    @post()
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
            )
        )
        await shop_repo.session.commit()
        return schemas.Shop.from_orm(obj)


class WebController(Controller):
    """Website rendering"""

    path = ""

    @get("/")
    async def homepage(self) -> Template:
        return Template(name="map.html.jinja2")
