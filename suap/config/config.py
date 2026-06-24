from typing import Optional

import tomllib
import logging
from pathlib import Path

from .data import ConfigData

__all__ = (
    "get_config_data",
)

logger = logging.getLogger(__name__)

def get_config_data(project_root_dir: Path) -> Optional[ConfigData]:
    config_path = project_root_dir.joinpath("suap.toml")

    if not config_path.exists():
        return None

    config_data: ConfigData = {}

    logger.debug(f"Opening and reading '{config_path.name}'...")

    with open(config_path, mode = "rb") as file:
        logger.debug("Parsing toml config...")
        config_data = tomllib.load(file)

    return config_data