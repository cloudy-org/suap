from typing import Optional

import os
import logging
from pathlib import Path
from subprocess import check_call, CalledProcessError

from ...platform_format import PlatformFormat

__all__ = (
    "get_cargo_toolchain",
    "build_cargo_project",
)

logger = logging.getLogger(__name__)

def get_cargo_toolchain(platform_format: PlatformFormat) -> Optional[str]:
    toolchain_name: Optional[str] = None

    if platform_format & PlatformFormat.LINUX:
        toolchain_name = "x86_64-unknown-linux-gnu"

    elif platform_format & PlatformFormat.WINDOWS:
        toolchain_name = "x86_64-pc-windows-gnu"

    elif platform_format & PlatformFormat.MACOS:
        # TODO: add and test macos support
        return None

    return toolchain_name

def build_cargo_project(
    toolchain_name: str,
    cargo_crate_name: str,
    icon_path: Path,
    temp_folder_path: Path
) -> bool:
    logger.debug(f"Invoking 'cargo build' with toolchain '{toolchain_name}'...")

    try:
        default_env = os.environ.copy()

        rust_flags = ["-Awarnings"] # hides warnings in console

        if toolchain_name == "x86_64-pc-windows-gnu":
            compiled_resource_path = build_windows_resource_file(icon_path, temp_folder_path)

            rust_flags.extend(["-C", f"link-arg={compiled_resource_path}"])

        default_env["RUSTFLAGS"] = " ".join(rust_flags)

        logger.warning(
            f"RUSTFLAGS is NOT inherited! 'RUSTFLAGS' will contain -> '{default_env['RUSTFLAGS']}'."
        )

        check_call(
            [
                "cargo",
                "build",
                "--release",
                "--package",
                cargo_crate_name,
                "--target",
                toolchain_name
            ],
            env = default_env
        )

    except CalledProcessError as error:
        logger.error(
            f"Failed to cargo build! Error: {error}"
        )

        return False

    return True

def build_windows_resource_file(icon_path: Path, temp_folder_path: Path) -> Optional[Path]:
    logger.debug("Building windows resource file...")

    resource_file_path = temp_folder_path.joinpath("resource.rc")
    compiled_resource_binary_path = temp_folder_path.joinpath("resource.res")

    resource_contents = f"""
IDI_MYICON ICON "{icon_path.absolute()}"
"""

    with open(resource_file_path, mode = "w") as file:
        file.write(resource_contents)

    try:
        logger.debug(f"Invoking 'x86_64-w64-mingw32-windres' to build '{compiled_resource_binary_path}'...")

        check_call(
            # now if you're using a distro that doesn't name 
            # windres as "x86_64-w64-mingw32-windres"... *Eh... your loss...*
            args = [
                "x86_64-w64-mingw32-windres",
                f"{resource_file_path.absolute()}",
                "-O",
                "coff",
                "-o",
                f"{compiled_resource_binary_path.absolute()}"
            ]
        )

    except CalledProcessError as error:
        logger.error(
            f"Failed to build windows resource file (resource.res)! Error: {error}"
        )

        return None

    return compiled_resource_binary_path