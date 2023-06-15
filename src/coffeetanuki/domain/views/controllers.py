from litestar import Controller, get
from litestar.response_containers import Template

from pydantic import parse_obj_as

from coffeetanuki.domain.shops.schemas import ShopDB
from coffeetanuki.domain.shops.repositories import ShopRepository, provide_shop_repo
from coffeetanuki.domain.shops.utils import geojsonify


class ViewsController(Controller):
    """Views rendering"""

    path = ""

    @get(
        path="/",
        include_in_schema=False,
    )
    async def home_page(self) -> Template:
        return Template(name="views/home.html.jinja")

    @get(
        path="/admin",
        include_in_schema=False,
    )
    async def admin_dash(self) -> Template:
        return Template("views/admin-dashboard.html.jinja")

    @get(
        path="/map",
        include_in_schema=False,
        dependencies={"shop_repo": provide_shop_repo},
    )
    async def map_page(
        self,
        shop_repo: ShopRepository,
    ) -> Template:
        shops = parse_obj_as(list[ShopDB], await shop_repo.list())
        shops_geojson = geojsonify(shops)
        return Template(
            name="views/map.html.jinja", context={"shops_geojson": shops_geojson}
        )
