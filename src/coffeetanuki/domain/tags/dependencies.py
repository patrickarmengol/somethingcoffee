from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from coffeetanuki.domain.tags.models import Tag

__all__ = ["TagRepository", "provide_tag_repo", "provide_r_tag_repo"]


class TagRepository(SQLAlchemyAsyncRepository[Tag]):
    """Tag Repository"""

    model_type = Tag


async def provide_tag_repo(db_session: AsyncSession) -> TagRepository:
    return TagRepository(session=db_session)


async def provide_r_tag_repo(db_session: AsyncSession) -> TagRepository:
    return TagRepository(
        statement=select(Tag).options(selectinload(Tag.shops)),
        session=db_session,
    )
