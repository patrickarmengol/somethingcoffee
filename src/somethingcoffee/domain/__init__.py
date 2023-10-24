from litestar.types import ControllerRouterHandler
from somethingcoffee.domain import shops, tags, home

__all__ = ["routes", "shops", "tags", "home"]

routes: list[ControllerRouterHandler] = [
    shops.routes.api.ShopAPIController,
    tags.routes.api.TagAPIController,
    shops.routes.views.ShopWebController,
    shops.routes.admin.ShopAdminController,
    tags.routes.admin.TagAdminController,
    home.routes.home_page,
    home.routes.map_page,
    home.routes.admin_dash,
]
