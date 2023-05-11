from asyncpg.pgproto import pgproto  # type: ignore
from litestar import Litestar
from litestar.serialization import DEFAULT_TYPE_ENCODERS

from coffeetanuki import domain
from coffeetanuki.database import sqlalchemy_plugin
from coffeetanuki.domain.web.configs import static_files_config, template_config

app = Litestar(
    route_handlers=[*domain.routes],
    plugins=[sqlalchemy_plugin],
    template_config=template_config,
    static_files_config=static_files_config,
    type_encoders={**DEFAULT_TYPE_ENCODERS, pgproto.UUID: str},
    debug=True,
)
