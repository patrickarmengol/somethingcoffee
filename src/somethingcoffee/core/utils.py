import pkgutil
from importlib.machinery import SourceFileLoader
from pathlib import Path


def module_to_os_path(dotted_path: str = "app") -> Path:
    """Find Module to OS Path.

    Return path to the base directory of the project or the module
    specified by `dotted_path`.

    Ensures that pkgutil returns a valid source file loader.
    """
    src = pkgutil.get_loader(dotted_path)
    if not isinstance(src, SourceFileLoader):
        raise TypeError("Couldn't find the path for %s", dotted_path)
    return Path(str(src.path).removesuffix("/__init__.py"))
