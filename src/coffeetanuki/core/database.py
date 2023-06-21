from litestar.contrib.sqlalchemy.plugins.init import (
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from coffeetanuki.core.settings import db

# create engine and session_maker manually to allow for expire_on_commit=False
engine = create_async_engine(db.URL)
async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    expire_on_commit=False,  # ensures joined attributes are available after commit
)

# setup sqla config and pass it to plugin
sqlalchemy_config = SQLAlchemyAsyncConfig(
    engine_instance=engine,
    session_maker=async_session_factory,
)
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)
