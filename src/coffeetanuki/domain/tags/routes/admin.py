from litestar import Controller, get
from litestar.di import Provide
from litestar.response import Template
from pydantic import parse_obj_as

from coffeetanuki.domain.tags.dependencies import TagRepository, provide_tag_repo
from coffeetanuki.domain.tags.schemas import TagDB


class TagAdminController(Controller):
    """Tag admin panel"""

    path = "/admin/tags"

    @get(
        path="/list",
        include_in_schema=False,
        dependencies={
            "tag_repo": Provide(provide_tag_repo),
        },
    )
    async def admin_tags_table(
        self,
        tag_repo: TagRepository,
    ) -> Template:
        table_name = "tags"
        data = parse_obj_as(list[TagDB], await tag_repo.list())
        cols = ["id", "name"]

        return Template(
            template_name="admin/admin-table.html.jinja",
            context={"table_name": table_name, "cols": cols, "data": data},
        )
