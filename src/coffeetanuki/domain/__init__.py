from litestar.types import ControllerRouterHandler
from coffeetanuki.domain import shops, views

__all__ = ["routes", "shops"]

routes: list[ControllerRouterHandler] = [
    shops.controllers.api.ShopAPIController,
    shops.controllers.api.AmenityAPIController,
    shops.controllers.web.ShopWebController,
    shops.controllers.admin.ShopAdminController,
    shops.controllers.admin.AmenityAdminController,
    views.controllers.ViewsController,
]
