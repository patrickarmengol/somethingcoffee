from uuid import UUID
from litestar import Controller, get
from litestar.di import Provide
from litestar.params import Parameter
from litestar.response import Template
from pydantic import parse_obj_as

from somethingcoffee.domain.shops.dependencies import ShopRepository, provide_shop_repo
from somethingcoffee.domain.shops.schemas import ShopDBFull
from somethingcoffee.domain.tags.dependencies import TagRepository, provide_tag_repo


class ShopAdminController(Controller):
    """Shop admin panel"""

    path = "/admin/shops"
    dependencies = {
        "shop_repo": Provide(provide_shop_repo),
        "tag_repo": Provide(provide_tag_repo),
    }

    @get(
        path="/list",
        include_in_schema=False,
    )
    async def admin_shops_table(
        self,
        shop_repo: ShopRepository,
    ) -> Template:
        shops = parse_obj_as(list[ShopDBFull], await shop_repo.list())
        return Template(
            template_name="admin/admin-shop-table.html.jinja",
            context={"shops": shops},
        )

    @get(
        path="/create",
        include_in_schema=False,
    )
    async def admin_shop_add(
        self,
        tag_repo: TagRepository,
    ) -> Template:
        return Template(
            template_name="admin/admin-shop-create.html.jinja",
            context={"tags": await tag_repo.list()},
        )

    @get(
        path="/{shop_id:uuid}/edit",
        include_in_schema=False,
    )
    async def admin_shop_edit(
        self,
        shop_repo: ShopRepository,
        tag_repo: TagRepository,
        shop_id: UUID = Parameter(
            title="Shop ID",
            description="The shop to retrieve",
        ),
    ) -> Template:
        shop = parse_obj_as(ShopDBFull, await shop_repo.get(shop_id))
        return Template(
            template_name="admin/admin-shop-edit.html.jinja",
            context={"shop": shop, "tags": await tag_repo.list()},
        )
