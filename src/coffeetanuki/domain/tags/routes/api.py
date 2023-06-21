from typing import Any
from uuid import UUID

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.params import Parameter
from litestar.contrib.repository.filters import CollectionFilter

from pydantic import parse_obj_as


from coffeetanuki.domain.tags.dependencies import (
    TagRepository,
    provide_tag_repo,
    provide_r_tag_repo,
)

from coffeetanuki.domain.tags.schemas import TagCreate, TagUpdate, TagDB, TagDBFull
from coffeetanuki.domain.tags.models import Tag


class TagAPIController(Controller):
    """Tag CRUD"""

    path = "/api/tags"
    dependencies = {
        "tag_repo": Provide(provide_tag_repo),
        "r_tag_repo": Provide(provide_r_tag_repo),
    }

    # list tags
    @get(
        path="",
        operation_id="ListTags",
        name="tags:list",
        summary="List all tags.",
        tags=["tags"],
    )
    async def list_tags(
        self,
        r_tag_repo: TagRepository,
    ) -> list[TagDBFull]:
        return parse_obj_as(list[TagDBFull], await r_tag_repo.list())

    # get tag by id
    @get(
        path="/{tag_id:uuid}",
        operation_id="GetTag",
        name="tags:get",
        summary="Get an tag by its ID.",
        tags=["tags"],
    )
    async def get_tag(
        self,
        r_tag_repo: TagRepository,
        tag_id: UUID = Parameter(
            title="Tag ID",
            description="Tag to retrieve",
        ),
    ) -> TagDBFull:
        return parse_obj_as(TagDBFull, await r_tag_repo.get(tag_id))

    # create tag
    @post(
        path="",
        operation_id="CreateTag",
        name="tags:create",
        summary="Create a new tag.",
        tags=["tags"],
    )
    async def create_tag(
        self,
        tag_repo: TagRepository,
        data: TagCreate,
    ) -> TagDB:
        obj = await tag_repo.add(Tag(**data.dict()))
        await tag_repo.session.commit()
        return parse_obj_as(TagDB, obj)

    # update tag
    @patch(
        path="/{tag_id:uuid}",
        operation_id="UpdateTag",
        name="tags:update",
        summary="Update an tag by its ID.",
        tags=["tags"],
    )
    async def update_tag(
        self,
        tag_repo: TagRepository,
        data: TagUpdate,
        tag_id: UUID = Parameter(
            title="Tag ID",
            description="The tag to update",
        ),
    ) -> TagDB:
        dd = data.dict(exclude_unset=True)
        dd.update({"id": tag_id})
        obj = await tag_repo.update(Tag(**dd))
        await tag_repo.session.commit()
        return parse_obj_as(TagDB, obj)

    # delete tag
    @delete(
        path="/{tag_id:uuid}",
        operation_id="DeleteTag",
        name="tags:delete",
        summary="Delete an tag by its ID.",
        tags=["tags"],
    )
    async def delete_tag(
        self,
        r_tag_repo: TagRepository,
        tag_id: UUID = Parameter(
            title="Tag ID",
            description="The tag to delete",
        ),
    ) -> None:
        _ = await r_tag_repo.delete(tag_id)
        await r_tag_repo.session.commit()
