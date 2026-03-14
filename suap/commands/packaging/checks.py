import re
import typer
import logging
from ...projects import ProjectData

__all__ = ()

logger = logging.getLogger(__name__)

def check_project_data_validity(project_data: ProjectData) -> None:
    project_name = project_data.name

    is_project_name_allowed = bool(
        re.fullmatch(r'^[a-zA-Z]+$', project_name)
    )

    if not is_project_name_allowed:
        logger.error(
            "Project name can only contain letters. Symbols, " \
                "numbers, spaces, dashes and etc are not allowed!"
        )

        raise typer.Exit(1)

    if any(char.isupper() for char in project_name):
        logger.error(
            "Project name must be all lowercase!"
        )

        raise typer.Exit(1)

    return None