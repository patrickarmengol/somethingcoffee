from litestar.types import ControllerRouterHandler
from coffeetanuki.domain import shops, web

__all__ = ["routes", "shops"]

routes: list[ControllerRouterHandler] = [
    shops.controllers.api.ShopAPIController,
    shops.controllers.api.AmenityAPIController,
    shops.controllers.web.ShopWebController,
    shops.controllers.admin.ShopAdminController,
    shops.controllers.admin.AmenityAdminController,
    web.handlers.home_page,
    web.handlers.map_page,
    web.handlers.admin_dash,
]
