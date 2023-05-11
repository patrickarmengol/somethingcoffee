from litestar.contrib.sqlalchemy.plugins.init import (
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)

# TODO: replace with env vars parsed in settings.py
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="postgresql+asyncpg://ctadmin:ctpass@localhost:5432/gis",
)
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)
