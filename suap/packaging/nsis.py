import shutil
import logging
from typer import Exit
from pathlib import Path

from ..projects import ProjectData
from ..formats import make_nsis_installer

__all__ = (
    "format_config_and_make_nsis_installer",
)

logger = logging.getLogger(__name__)

def format_config_and_make_nsis_installer(
    binary_path: Path,
    binary_name: str,
    binary_suffix: str,
    dist_folder_path: Path,
    temp_folder_path: Path,
    project_data: ProjectData,
):
    logger.debug(
        "Formatting NSIS template installer script with suap project data..."
    )

    dist_folder_path.mkdir(exist_ok = True)
    binary_dist_path = dist_folder_path.joinpath(f"{binary_name}-{binary_suffix}")

    temp_folder_path.mkdir(exist_ok = True)
    nsis_installer_script_path = temp_folder_path.joinpath("nsis_installer.nsi")

    installer_script_template_path = Path(__file__).parent.parent.joinpath(
        "templates", "nsis_installer_script.nsi"
    )

    logger.debug(
        f"Opening and reading NSIS template installer script at '{installer_script_template_path}'..."
    )

    with open(installer_script_template_path, mode = "r") as file:
        installer_script_string = file.read()

    logger.debug("Formatting template and creating custom install script...")

    semver = project_data.version

    replace_map: dict[str, str] = {
        "suap-binary-name": binary_name,
        "suap-binary-path": f"../{binary_path}",
        "suap-binary-dist-path": str(binary_dist_path),

        "suap-project-name": project_data.name,
        "suap-project-version": f"{semver.major}.{semver.minor}.{semver.patch}" \
            f".{semver.prerelease.split('.')[-1] if semver.prerelease is not None else 0}",
        "suap-project-description": project_data.description,
    }

    for (suap_key, value) in replace_map.items():
        installer_script_string = installer_script_string.replace(f"{{{suap_key}}}", value)

    logger.debug(
        f"Creating and writing to custom NSIS installer script at '{nsis_installer_script_path}'..."
    )

    with open(nsis_installer_script_path, mode = "w") as file:
        file.write(installer_script_string)

    if not make_nsis_installer(nsis_installer_script_path):
        raise Exit(1)

    logger.debug("Done making NSIS installer, installer executable should be in dist.")

    logger.debug("Removing temp dir...")

    shutil.rmtree(temp_folder_path)