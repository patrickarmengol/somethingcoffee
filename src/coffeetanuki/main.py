from litestar import Litestar
from litestar.serialization import DEFAULT_TYPE_ENCODERS
from coffeetanuki.database import sqlalchemy_plugin
from coffeetanuki.controllers import ShopController, WebController
from asyncpg.pgproto import pgproto  # type: ignore
from coffeetanuki.templating import template_config, static_files_config


app = Litestar(
    route_handlers=[ShopController, WebController],
    plugins=[sqlalchemy_plugin],
    template_config=template_config,
    static_files_config=static_files_config,
    type_encoders={**DEFAULT_TYPE_ENCODERS, pgproto.UUID: str},
    debug=True,
)
