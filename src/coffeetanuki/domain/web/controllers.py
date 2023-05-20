from uuid import UUID
from litestar import Controller, get
from litestar.response_containers import Template


class WebController(Controller):
    """Website rendering"""

    path = ""

    @get(path="/map", include_in_schema=False)
    async def homepage(self) -> Template:
        return Template(name="map.html.jinja2")

    @get(path="/shops", include_in_schema=False)
    async def shops_list_page(self) -> Template:
        return Template(name="shops_list.html.jinja2")

    @get(path="/shops/{shop_id:uuid}", include_in_schema=False)
    async def shop_details_page(self, shop_id: UUID) -> Template:
        return Template(name="shop.html.jinja2")
