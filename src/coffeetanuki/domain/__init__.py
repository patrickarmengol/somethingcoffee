from litestar.types import ControllerRouterHandler
from coffeetanuki.domain import shops, web, admin

__all__ = ["routes", "shops", "web"]

routes: list[ControllerRouterHandler] = [
    shops.controllers.ShopAPIController,
    shops.controllers.AmenityAPIController,
    shops.controllers.ShopWebController,
    web.controllers.WebController,
    admin.controllers.AdminController,
]
