from litestar import Litestar

from somethingcoffee import domain
from somethingcoffee.core.database import sqlalchemy_plugin
from somethingcoffee.ui.configs import static_files_config, template_config

app = Litestar(
    route_handlers=[*domain.routes],
    plugins=[sqlalchemy_plugin],
    template_config=template_config,
    static_files_config=static_files_config,
    debug=True,
)
