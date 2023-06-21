from uuid import UUID
from litestar import Controller, get
from litestar.di import Provide
from litestar.params import Parameter
from litestar.response import Template
from pydantic import parse_obj_as

from coffeetanuki.domain.shops.dependencies import ShopRepository, provide_shop_repo
from coffeetanuki.domain.shops.schemas import ShopDB, ShopDBFull


class ShopAdminController(Controller):
    """Shop admin panel"""

    path = "/admin/shops"
    dependencies = {"shop_repo": Provide(provide_shop_repo)}

    @get(
        path="/list",
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
            template_name="views/admin-table.html.jinja",
            context={"table_name": table_name, "cols": cols, "data": data},
        )

    @get(
        path="/create",
        include_in_schema=False,
    )
    async def admin_shop_add(
        self,
    ) -> Template:
        return Template(template_name="views/admin-create-shop.html.jinja")

    @get(
        path="/{shop_id:uuid}/edit",
        include_in_schema=False,
    )
    async def admin_shop_edit(
        self,
        shop_repo: ShopRepository,
        shop_id: UUID = Parameter(
            title="Shop ID",
            description="The shop to retrieve",
        ),
    ) -> Template:
        shop = parse_obj_as(ShopDBFull, await shop_repo.get(shop_id))
        return Template(
            template_name="views/admin-edit-shop.html.jinja", context={"shop": shop}
        )