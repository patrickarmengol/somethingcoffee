from uuid import UUID
from litestar import Controller, get
from litestar.di import Provide
from litestar.params import Parameter
from litestar.response_containers import Template

from pydantic import parse_obj_as

from coffeetanuki.domain.shops.dependencies import (
    ShopRepository,
    provide_shop_repo,
    provide_r_shop_repo,
)
from coffeetanuki.domain.shops.schemas import ShopDBFull


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
        shops = parse_obj_as(list[ShopDBFull], await r_shop_repo.list())
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
        shop = parse_obj_as(ShopDBFull, await r_shop_repo.get(shop_id))
        return Template("views/shop-details.html.jinja", context={"shop": shop})
