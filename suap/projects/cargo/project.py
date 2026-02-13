from typing import Optional

import json
import logging
from pathlib import Path
from subprocess import check_output, CalledProcessError

from ..data import ProjectData

from .metadata_data import CargoMetadataData

__all__ = (
    "get_cargo_project_data",
)

logger = logging.getLogger(__name__)

def get_cargo_project_data(cargo_crate_name: str) -> Optional[ProjectData]:
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

        if cargo_package.name == cargo_crate_name:
            return ProjectData(
                name = cargo_package.name
            )

    logger.error(f"Cargo package was not found with the name '{cargo_crate_name}'!")

    return None