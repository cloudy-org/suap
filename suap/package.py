from typing import Annotated, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from config.data import ProjectData

import os
import logging
from enum import StrEnum
from pathlib import Path
from typer import Option, Typer, Exit

from .config import get_config_data
from .projects import get_cargo_project_data

__all__ = ()

app = Typer()
logger = logging.getLogger(__name__)

class ProjectType(StrEnum):
    CARGO = "cargo"

class PlatformFormat(StrEnum):
    LINUX = "linux"

    WINDOWS = "windows"
    WINDOWS_BINARY = "windows-bin"
    WINDOWS_SETUP = "windows-setup"

    MACOS = "macos"

@app.command()
def package(
    project: Annotated[ProjectType, Option(help = "Which project should we package (e.g: the cargo project, python project?).")],
    platform_format: Annotated[
        PlatformFormat,
        Option(
            help = "The packaging format or platform we are targeting. Choose a less generic option if you only want to " \
                "package towards ONE specific format such as 'windows-setup', otherwise all available formats " \
                "of such platform will be automatically packaged."
        )
    ],
    bin_output_name: Annotated[
        Optional[str],
        Option(
            help = "Override the default project name prefixed in front of the binary name " \
                "(e.g: 'name-linux-x86_64', 'name-win-x86_64-setup.exe', 'name-macos-x86_64')."
        )
    ] = None,
):
    current_working_directory = Path(os.getcwd())

    logger.debug("Getting config data...")
    config_data = get_config_data(current_working_directory)

    if config_data is None:
        logger.error(
            "'suap.toml' does not exist in current working " \
                f"directory! (CWD: {current_working_directory})"
        )
        raise Exit(1)

    if project == ProjectType.CARGO:
        projects_data: Optional[ProjectData] = config_data.get("project", None)

        cargo_crate_name: Optional[str] = None

        if projects_data is not None:
            cargo_config_data = projects_data.get("cargo", None)

            if cargo_config_data is not None:
                cargo_crate_name = cargo_config_data.get("bin-crate", None)

        if cargo_crate_name is None:
            logger.error("Cargo 'bin-crate 'key was not set in '[project.cargo]'!")
            raise Exit(1)

        logger.info("Getting cargo project data...")
        project_data = get_cargo_project_data(cargo_crate_name)

        if project_data is None:
            raise Exit(1)

        # TODO: cargo build with project name and the correct platform
        # TODO: copy built binaries into dist folder in correct formatting and naming
        # TODO: package special types of formats correctly (e.g: windows-setup, generate configs for NSIS)

    print("WIP!")