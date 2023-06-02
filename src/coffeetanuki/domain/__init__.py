from litestar.types import ControllerRouterHandler
from coffeetanuki.domain import shops, web

__all__ = ["routes", "shops", "web"]

routes: list[ControllerRouterHandler] = [
    shops.controllers.ShopAPIController,
    shops.controllers.AmenityAPIController,
    web.controllers.WebController,
]
