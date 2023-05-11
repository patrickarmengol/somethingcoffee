from litestar.contrib.sqlalchemy.plugins.init import (
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)

from coffeetanuki.settings import db

# TODO: replace with env vars parsed in settings.py
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=db.URL,
)
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)
