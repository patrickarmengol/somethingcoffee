from uuid import UUID
from litestar import Controller, get
from litestar.di import Provide
from litestar.params import Parameter
from litestar.response import Template
from pydantic import parse_obj_as

from somethingcoffee.domain.tags.dependencies import TagRepository, provide_tag_repo
from somethingcoffee.domain.tags.schemas import TagDBFull


class TagAdminController(Controller):
    """Tag admin panel"""

    path = "/admin/tags"
    dependencies = {"tag_repo": Provide(provide_tag_repo)}

    @get(
        path="/list",
        include_in_schema=False,
    )
    async def admin_tags_table(
        self,
        tag_repo: TagRepository,
    ) -> Template:
        tags = parse_obj_as(list[TagDBFull], await tag_repo.list())
        return Template(
            template_name="admin/admin-tag-table.html.jinja",
            context={"tags": tags},
        )

    @get(
        path="/create",
        include_in_schema=False,
    )
    async def admin_tag_create(
        self,
    ) -> Template:
        return Template(template_name="admin/admin-tag-create.html.jinja")

    @get(
        path="/{tag_uuid:uuid}/edit",
        include_in_schema=False,
    )
    async def admin_tag_edit(
        self,
        tag_repo: TagRepository,
        tag_uuid: UUID = Parameter(
            title="Tag ID",
            description="The tag to retrieve.",
        ),
    ) -> Template:
        tag = parse_obj_as(TagDBFull, await tag_repo.get(tag_uuid))
        return Template(
            template_name="admin/admin-tag-edit.html.jinja",
            context={"tag": tag},
        )
