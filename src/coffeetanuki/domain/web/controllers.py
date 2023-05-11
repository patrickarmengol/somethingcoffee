from litestar import Controller, get
from litestar.response_containers import Template


class WebController(Controller):
    """Website rendering"""

    path = ""

    @get("/map")
    async def homepage(self) -> Template:
        return Template(name="map.html.jinja2")
