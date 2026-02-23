import logging
from pathlib import Path
from subprocess import check_call, CalledProcessError

__all__ = (
    "make_nsis_installer",
)

logger = logging.getLogger(__name__)

def make_nsis_installer(install_script_path: Path) -> bool:
    logger.debug(f"Running 'makensis' with custom install script ('{install_script_path}')...")

    try:
        check_call(
            [
                "makensis",
                str(install_script_path),
            ]
        )

    except CalledProcessError as error:
        logger.error(
            f"Failed to make nsis installer! Error: {error}"
        )

        return False

    return True