from typing import Optional

import os
import logging
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

def build_cargo_project(toolchain_name: str, cargo_crate_name: str) -> bool:
    logger.debug(f"Invoking 'cargo build' with toolchain '{toolchain_name}'...")

    try:
        default_env = os.environ.copy()
        default_env["RUSTFLAGS"] = "-Awarnings" # hides warnings in console

        logger.warning(
            f"RUSTFLAGS are not inherited! 'RUSTFLAGS' will contain -> '{default_env['RUSTFLAGS']}'."
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