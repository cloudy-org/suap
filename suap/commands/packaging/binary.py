import shutil
import logging
from pathlib import Path

__all__ = ()

logger = logging.getLogger(__name__)

def format_and_copy_binary_to_dist(
    binary_path: Path,
    binary_name: str,
    binary_suffix: str,
    dist_folder_path: Path,
):
    logger.debug(
        f"Formatting binary with name '{binary_name}' and suffix '{binary_suffix}'..."
    )

    dist_folder_path.mkdir(exist_ok = True)

    binary_dist_path = dist_folder_path.joinpath(f"{binary_name}-{binary_suffix}")

    logger.debug(
        f"Copying built binary into dist folder formatted as '{binary_dist_path.name}'..."
    )
    shutil.copy(binary_path, binary_dist_path)