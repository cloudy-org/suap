from typing import Optional

import shutil
import logging
from pathlib import Path

from ...platform_format import PlatformFormat

__all__ = ()

logger = logging.getLogger(__name__)

def get_platform_icon_path(icons_path: Path, platform_format: PlatformFormat) -> Optional[Path]:
    """
    Returns `None` if an icon can't be found / doesn't exist. Otherwise a `Path` is returned.
    """
    icon_file_name = None

    if platform_format & PlatformFormat.LINUX:
        icon_file_name = "linux.png"

    elif platform_format & PlatformFormat.WINDOWS:
        icon_file_name = "windows.ico"

    elif platform_format & PlatformFormat.MACOS:
        icon_file_name = "macos.icns"

    if icon_file_name is not None:
        icon_image_path = icons_path.joinpath(icon_file_name)

        if icon_image_path.exists():
            logger.debug(f"Platform specific icon was found at '{icon_image_path}'.")

            return icon_image_path

        original_icon_path = icons_path.joinpath("original.png")

        if original_icon_path.exists():
            logger.warning(
                "No platform specific icons were found! Falling " \
                f"back to 'original' icon ({original_icon_path})..."
            )

            if platform_format & PlatformFormat.WINDOWS:
                logger.warning(
                    "You will MOST LIKELY want a platform specific icon for Windows "\
                        "(e.g: 'windows.ico') as support for PNGs are a gray area and can cause problems."
                )

            return original_icon_path

    return None

def format_icon_with_project_name(
    icon_path: Path,
    temp_folder_path: Path,
    project_name: str
) -> Path:
    logger.debug(
        "Formatting icon with project name and " \
            "copying it over to the './temp' directory..."
    )

    temp_folder_path.mkdir(exist_ok = True)

    icon_temp_destination_path = temp_folder_path.joinpath(
        f"{project_name}{icon_path.suffix}"
    )

    logger.debug(f"Copying icon to temp directory at '{icon_temp_destination_path}'...")

    shutil.copy(icon_path, icon_temp_destination_path)

    return icon_temp_destination_path