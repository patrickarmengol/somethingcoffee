from typing import Any
from litestar import Controller, get
from litestar.di import Provide
from litestar.response_containers import Template
from pydantic import parse_obj_as

from coffeetanuki.domain.shops.controllers import (
    AmenityRepository,
    ShopRepository,
    provide_amenity_repo,
    provide_shop_repo,
)
from coffeetanuki.domain.shops.schemas import AmenityDB, ShopDB


class AdminController(Controller):
    """Admin panel"""

    path = "/admin"

    @get(
        path="",
        include_in_schema=False,
    )
    async def admin_dash(
        self,
    ) -> Template:
        return Template("views/admin-dashboard.html.jinja")

    @get(
        path="tables/{table_name:str}",
        include_in_scheema=False,
        dependencies={
            "shop_repo": Provide(provide_shop_repo),
            "amenity_repo": Provide(provide_amenity_repo),
        },
    )
    async def admin_table(
        self,
        shop_repo: ShopRepository,
        amenity_repo: AmenityRepository,
        table_name: str,
    ) -> Template:
        data: list[Any] = []
        cols: list[str] = []  # hardcode cols
        if table_name == "shops":
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
        elif table_name == "amenities":
            data = parse_obj_as(list[AmenityDB], await amenity_repo.list())
            cols = [
                "id",
                "name",
            ]

        return Template(
            "views/admin-table.html.jinja",
            context={"table_name": table_name, "cols": cols, "data": data},
        )
