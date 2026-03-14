from typing import Annotated, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ...config.data import ConfigProjectData

import os
import shutil
import logging
from pathlib import Path
from typer import Option, Typer, Exit

from .checks import check_project_data_validity
from .binary import format_and_copy_binary_to_dist
from .nsis import format_config_and_make_nsis_installer
from .icons import get_platform_icon_path, format_icon_with_project_name

from ...mime_type import MimeType
from ...config import get_config_data
from ...project_type import ProjectType
from ...platform_format import PlatformFormat, PlatformFormatOption
from ...projects import find_and_get_cargo_project_data, build_cargo_project, get_cargo_toolchain

__all__ = ("app",)

app = Typer()
logger = logging.getLogger(__name__)

@app.command()
def package(
    project: Annotated[ProjectType, Option(help = "Which project should we package (e.g: the cargo project, python project?).")],
    platform_format: Annotated[
        PlatformFormatOption,
        Option(
            help = "The packaging format or platform we are targeting. Choose a less generic option if you only want to " \
                "package towards ONE specific format such as 'windows-setup', otherwise all available formats " \
                "of such platform will be automatically packaged (as is the case with 'windows')."
        )
    ],
    bin_output_name: Annotated[
        Optional[str],
        Option(
            help = "Override the default binary name prefixed in front of the binary suffix " \
                "(e.g: 'bin-name-linux-x86_64', 'bin-name-win-x86_64-setup.exe', 'bin-name-macos-x86_64')."
        )
    ] = None,
    remove_temp: bool = True,
):
    platform_format: PlatformFormat = platform_format.get_platform_format()

    current_working_directory = Path(os.getcwd())

    dist_folder_path = current_working_directory.joinpath("dist")
    temp_folder_path = current_working_directory.joinpath("temp")

    logger.debug("Getting config data...")
    config_data = get_config_data(current_working_directory)

    if config_data is None:
        raise Exit(1)

    # TODO: move this stuff to some sort of Config class
    display_name: Optional[str] = config_data.get("display-name", None)
    icons_config_path: Optional[str] = config_data.get("icons", None)
    mime_types: list[MimeType] = [
        MimeType(mime_type_string = mime_type) for mime_type in config_data.get("mime_types", [])
    ]

    if icons_config_path is None:
        logger.error(
            "Icons folder is required to be specific in the config and at " \
                "least an original icon must be present (e.g: 'original.png')!" \
                    '\n    icons = "./assets/icons"'
        )
        raise Exit(1)

    icons_path = Path(icons_config_path)

    if not icons_path.exists():
        logger.error(f"Icons folder path does not exist ('{icons_path}')!")

        raise Exit(1)

    platform_icon_path = get_platform_icon_path(icons_path, platform_format)

    if platform_icon_path is None:
        logger.error(
            "At least an original icon is required in your icons " \
                f"path at '{icons_config_path}' (e.g: 'original.png')!"
        )
        raise Exit(1)

    if project == ProjectType.CARGO:
        projects_config_data: Optional[ConfigProjectData] = config_data.get("project", None)

        cargo_crate_name: Optional[str] = None

        if projects_config_data is not None:
            cargo_config_data = projects_config_data.get("cargo", None)

            if cargo_config_data is not None:
                cargo_crate_name = cargo_config_data.get("bin-crate", None)

        if cargo_crate_name is None:
            logger.error("Cargo 'bin-crate 'key was not set in '[project.cargo]'!")
            raise Exit(1)

        logger.info("Getting cargo project data...")
        project_data = find_and_get_cargo_project_data(cargo_crate_name)

        if project_data is None:
            raise Exit(1)

        check_project_data_validity(project_data)

        toolchain_name = get_cargo_toolchain(platform_format)

        if toolchain_name is None:
            logger.error(
                "We don't support a cargo toolchain for this " \
                    f"platform format ({platform_format.name}) yet!"
            )
            raise Exit(1)

        if not build_cargo_project(toolchain_name, project_data.name):
            raise Exit(1)

        cargo_release_path = Path(f"./target/{toolchain_name}/release")

        binary_name = bin_output_name if bin_output_name is not None else project_data.name

        if platform_format & PlatformFormat.LINUX_BIN:
            binary_path = cargo_release_path.joinpath(project_data.name)

            format_and_copy_binary_to_dist(
                binary_path,
                binary_name = binary_name,
                binary_suffix = "linux-x86_64",
                dist_folder_path = dist_folder_path,
            )

        if platform_format & PlatformFormat.WINDOWS_BIN:
            binary_path = cargo_release_path.joinpath(f"{project_data.name}.exe")

            format_and_copy_binary_to_dist(
                binary_path,
                binary_name = binary_name,
                binary_suffix = "win-x86_64.exe",
                dist_folder_path = dist_folder_path,
            )

        if platform_format & PlatformFormat.WINDOWS_SETUP:
            binary_path = cargo_release_path.joinpath(f"{project_data.name}.exe")

            platform_icon_path = format_icon_with_project_name(
                platform_icon_path,
                temp_folder_path,
                project_name = project_data.name
            )

            format_config_and_make_nsis_installer(
                binary_path,
                binary_name = binary_name,
                binary_suffix = "win-x86_64-setup.exe",
                dist_folder_path = dist_folder_path,
                temp_folder_path = temp_folder_path,
                display_name = display_name,
                icon_path = platform_icon_path,
                mime_types = mime_types,
                project_data = project_data,
            )

    if remove_temp:
        logger.debug("Removing temp dir...")
        shutil.rmtree(temp_folder_path, ignore_errors = True)

    logger.info("This command is WIP!")