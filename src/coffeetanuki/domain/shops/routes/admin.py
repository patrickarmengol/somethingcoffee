from uuid import UUID
from litestar import Controller, get
from litestar.di import Provide
from litestar.params import Parameter
from litestar.response import Template
from pydantic import parse_obj_as
from pydantic.json import pydantic_encoder
import json

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
        shops = parse_obj_as(list[ShopDB], await shop_repo.list())
        shop_data = json.dumps(shops, default=pydantic_encoder)
        return Template(
            template_name="admin/admin-shop-table.html.jinja",
            context={"shop_data": shop_data},
        )

    @get(
        path="/create",
        include_in_schema=False,
    )
    async def admin_shop_add(
        self,
    ) -> Template:
        return Template(template_name="admin/admin-shop-create.html.jinja")

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
            template_name="admin/admin-shop-edit.html.jinja", context={"shop": shop}
        )
