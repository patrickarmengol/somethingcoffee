from litestar.types import ControllerRouterHandler
from coffeetanuki.domain import shops, home

__all__ = ["routes", "shops"]

routes: list[ControllerRouterHandler] = [
    shops.routes.api.ShopAPIController,
    shops.routes.api.AmenityAPIController,
    shops.routes.views.ShopWebController,
    shops.routes.admin.ShopAdminController,
    shops.routes.admin.AmenityAdminController,
    home.routes.home_page,
    home.routes.map_page,
    home.routes.admin_dash,
]
