from litestar.contrib.sqlalchemy.plugins import AsyncSessionConfig
from litestar.contrib.sqlalchemy.plugins.init import (
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from coffeetanuki.settings import db

engine = create_async_engine(db.URL)

async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

# TODO: replace with env vars parsed in settings.py
sqlalchemy_config = SQLAlchemyAsyncConfig(
    engine_instance=engine,
    session_maker=async_session_factory,
)
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)
