from litestar.types import ControllerRouterHandler
from coffeetanuki.domain import shops, web

__all__ = ["routes", "shops", "web"]

routes: list[ControllerRouterHandler] = [
    shops.controllers.ShopController,
    web.controllers.WebController,
]
