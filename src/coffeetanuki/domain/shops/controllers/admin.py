from litestar import Controller, get
from litestar.di import Provide
from litestar.response_containers import Template
from pydantic import parse_obj_as

from coffeetanuki.domain.shops.repositories import (
    AmenityRepository,
    ShopRepository,
    provide_amenity_repo,
    provide_shop_repo,
)
from coffeetanuki.domain.shops.schemas import AmenityDB, ShopDB


class ShopAdminController(Controller):
    """Shop admin panel"""

    path = "/admin/shops"
    dependencies = {"shop_repo": Provide(provide_shop_repo)}

    @get(
        path="",
        include_in_schema=False,
    )
    async def admin_shops_table(
        self,
        shop_repo: ShopRepository,
    ) -> Template:
        table_name = "shops"
        # should data be list of dicts instead of pydantic models?
        data = parse_obj_as(list[ShopDB], await shop_repo.list())
        cols = [
            "id",
            "name",
            "address",
            "coordinates.lon",
            "coordinates.lat",
            "roaster",
            "hours_of_operation",
            "description",
        ]

        return Template(
            "views/admin-table.html.jinja",
            context={"table_name": table_name, "cols": cols, "data": data},
        )


class AmenityAdminController(Controller):
    """Amenity admin panel"""

    path = "/admin/amenities"

    @get(
        path="",
        include_in_schema=False,
        dependencies={
            "amenity_repo": Provide(provide_amenity_repo),
        },
    )
    async def admin_amenities_table(
        self,
        amenity_repo: AmenityRepository,
    ) -> Template:
        table_name = "amenities"
        data = parse_obj_as(list[AmenityDB], await amenity_repo.list())
        cols = ["id", "name"]

        return Template(
            "views/admin-table.html.jinja",
            context={"table_name": table_name, "cols": cols, "data": data},
        )
