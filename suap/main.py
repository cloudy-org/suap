from typing import Annotated

import os
import logging
from pathlib import Path
from enum import StrEnum
from typer import Option, Typer, Exit

from logger import LogFormatter
from projects import get_cargo_project_data

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

@app.callback()
def callback():
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(LogFormatter())

    logging.basicConfig(
        format = "[%(levelname)s] %(message)s",
        level = logging.DEBUG,
        handlers = [log_handler]
    )

@app.command()
def package(
    project: Annotated[str, Option(help = "The name of the cargo package / project to build and package.")],
    project_type: Annotated[ProjectType, Option(help = "The type of project we're packaging (e.g: a cargo or python project).")],
    platform_format: Annotated[
        PlatformFormat,
        Option(
            help = "The packaging format or platform we are targeting. Choose a less generic option if you only want to " \
                "package towards ONE specific format such as 'windows-setup', otherwise all available formats will be automatically packaged."
        )
    ],
):
    current_working_directory = Path(os.getcwd())

    if project_type == ProjectType.CARGO:
        logger.info("Getting cargo project data...")
        project_data = get_cargo_project_data(current_working_directory, project)

        if project_data is None:
            raise Exit(1)

        # TODO: cargo build with project name and the correct platform
        # TODO: copy built binaries into dist folder in correct formatting and naming
        # TODO: package special types of formats correctly (e.g: windows-setup, generate configs for NSIS)

    print("WIP!")

@app.command(hidden = True) # WIP
def tools():
    ...

if __name__ == "__main__":
    app()