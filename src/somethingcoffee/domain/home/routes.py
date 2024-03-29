from litestar import get
from litestar.response import Template
from pydantic import parse_obj_as

from somethingcoffee.domain.shops.schemas import ShopDBFull
from somethingcoffee.domain.shops.dependencies import ShopRepository, provide_shop_repo
from somethingcoffee.domain.shops.utils import geojsonify


@get(
    path="/",
    include_in_schema=False,
)
async def home_page() -> Template:
    return Template(template_name="views/home.html.jinja")


@get(
    path="/map",
    include_in_schema=False,
    dependencies={"shop_repo": provide_shop_repo},
)
async def map_page(
    shop_repo: ShopRepository,
) -> Template:
    shops = parse_obj_as(list[ShopDBFull], await shop_repo.list())
    shops_geojson = geojsonify(shops)
    return Template(
        template_name="views/map.html.jinja", context={"shops_geojson": shops_geojson}
    )


@get(
    path="/admin",
    include_in_schema=False,
)
async def admin_dash() -> Template:
    return Template(template_name="admin/admin-dashboard.html.jinja")
