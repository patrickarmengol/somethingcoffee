from litestar import Controller, get
from litestar.response_containers import Template

from pydantic import parse_obj_as

from coffeetanuki.domain.shops.schemas import ShopDB
from coffeetanuki.domain.shops.repositories import ShopRepository, provide_shop_repo
from coffeetanuki.domain.shops.utils import geojsonify


@get(
    path="/",
    include_in_schema=False,
)
async def home_page() -> Template:
    return Template(name="views/home.html.jinja")


@get(
    path="/map",
    include_in_schema=False,
    dependencies={"shop_repo": provide_shop_repo},
)
async def map_page(
    shop_repo: ShopRepository,
) -> Template:
    shops = parse_obj_as(list[ShopDB], await shop_repo.list())
    shops_geojson = geojsonify(shops)
    return Template(
        name="views/map.html.jinja", context={"shops_geojson": shops_geojson}
    )


@get(
    path="/admin",
    include_in_schema=False,
)
async def admin_dash() -> Template:
    return Template(name="views/admin-dashboard.html.jinja")