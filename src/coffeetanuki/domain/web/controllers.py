from litestar import Controller, get
from litestar.response_containers import Template


class WebController(Controller):
    """General webpage rendering"""

    path = ""

    @get(path="/", include_in_schema=False)
    async def home_page(self) -> Template:
        return Template(name="views/home.html.jinja")

    @get(path="/map", include_in_schema=False)
    async def map_page(self) -> Template:
        return Template(name="views/map.html.jinja")
