from typing import Optional

import json
import logging
from subprocess import check_output, check_call, CalledProcessError

from ..data import ProjectData

from ...platform_format import PlatformFormat

from .metadata_data import CargoMetadataData

__all__ = (
    "find_and_get_cargo_project_data",
    "build_cargo_project",
    "get_cargo_toolchain",
)

logger = logging.getLogger(__name__)

def get_cargo_toolchain(platform_format: PlatformFormat) -> Optional[str]:
    toolchain_name: Optional[str] = None

    if platform_format.value.startswith("linux"):
        toolchain_name = "x86_64-unknown-linux-gnu"

    elif platform_format.value.startswith("windows"):
        toolchain_name = "x86_64-pc-windows-gnu"

    elif platform_format.value.startswith("macos"):
        raise NotImplementedError()

    return toolchain_name

def build_cargo_project(toolchain_name: str, cargo_crate_name: str) -> bool:
    logger.debug("Invoking 'cargo build'...")

    try:
        check_call(
            [
                "cargo",
                "build",
                "--release",
                "--package",
                cargo_crate_name,
                "--target",
                toolchain_name
            ]
        )

    except CalledProcessError as error:
        logger.error(
            f"Failed to cargo build! Error: {error}"
        )

        return False

    return True

def find_and_get_cargo_project_data(cargo_crate_name: str) -> Optional[ProjectData]:
    args = ["cargo", "metadata", "--no-deps", "--format-version", "1"]

    logger.debug("Running cargo metadata command to retrieve cargo project information...")

    try:
        json_string = check_output(args, text = True)

    except CalledProcessError as error:
        logger.error(
            f"Failed to execute 'cargo metadata'! Error: {error}"
        )

        return None

    cargo_metadata_data: CargoMetadataData = json.loads(json_string)

    for cargo_package in cargo_metadata_data["packages"]:

        if cargo_package["name"] == cargo_crate_name:
            return ProjectData(
                name = cargo_package["name"]
            )

    logger.error(f"Cargo package was not found with the name '{cargo_crate_name}'!")

    return None