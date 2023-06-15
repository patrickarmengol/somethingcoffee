from pathlib import Path
from typing import Final

from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import StaticFilesConfig
from litestar.template.config import TemplateConfig

from coffeetanuki.utils import module_to_os_path

__all__ = ["template_config", "static_files_config"]

DEFAULT_MODULE_NAME = "coffeetanuki"
BASE_DIR: Final = module_to_os_path(DEFAULT_MODULE_NAME)
TEMPLATES_DIR = Path(BASE_DIR / "web" / "templates")
SCRIPTS_DIR = Path(BASE_DIR / "web" / "static" / "scripts")
STYLES_DIR = Path(BASE_DIR / "web" / "static" / "styles")
IMAGES_DIR = Path(BASE_DIR / "web" / "static" / "images")


template_config = TemplateConfig(
    directory=TEMPLATES_DIR,
    engine=JinjaTemplateEngine,
)


static_files_config = [
    StaticFilesConfig(
        name="scripts",
        directories=[SCRIPTS_DIR],
        path="/scripts",
    ),
    StaticFilesConfig(
        name="styles",
        directories=[STYLES_DIR],
        path="/styles",
    ),
    StaticFilesConfig(
        name="images",
        directories=[IMAGES_DIR],
        path="/images",
    ),
]
