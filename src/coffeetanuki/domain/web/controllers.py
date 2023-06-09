from litestar import Controller, get
from litestar.di import Provide
from litestar.response_containers import Template
from pydantic import parse_obj_as

from coffeetanuki.domain.shops.utils import geojsonify
from coffeetanuki.domain.shops.controllers import (
    ShopRepository,
    provide_shop_repo,
    schemas,
)


class WebController(Controller):
    """General webpage rendering"""

    path = ""

    @get(path="/", include_in_schema=False)
    async def home_page(self) -> Template:
        return Template(name="views/home.html.jinja")

    @get(
        path="/map",
        include_in_schema=False,
        dependencies={"shop_repo": Provide(provide_shop_repo)},
    )
    async def map_page(self, shop_repo: ShopRepository) -> Template:
        shops = parse_obj_as(list[schemas.ShopDB], await shop_repo.list())
        shops_geojson = geojsonify(shops)
        return Template(
            name="views/map.html.jinja", context={"shops_geojson": shops_geojson}
        )
