from typing import Optional

import logging
from typer import Exit
from pathlib import Path

# just so we can get the root path of our library
import suap

from ...mime_type import MimeType
from ...projects import ProjectData
from ...formats import make_nsis_installer

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
    display_name: Optional[str],
    icon_path: Path,
    mime_types: list[MimeType],
    project_data: ProjectData,
):
    logger.debug(
        "Formatting NSIS template installer script with suap project data..."
    )

    dist_folder_path.mkdir(exist_ok = True)
    binary_dist_path = dist_folder_path.joinpath(f"{binary_name}-{binary_suffix}")

    temp_folder_path.mkdir(exist_ok = True)
    nsis_installer_script_path = temp_folder_path.joinpath("nsis_installer.nsi")

    templates_path = Path(suap.__file__).parent.joinpath("templates")
    installer_script_template_path = templates_path.joinpath("nsis_installer_script.nsi")

    logger.debug(
        f"Opening and reading NSIS template installer script at '{installer_script_template_path}'..."
    )

    with open(installer_script_template_path, mode = "r") as file:
        installer_script_string = file.read()

    logger.debug("Formatting template and creating custom install script...")

    semver = project_data.version
    display_name = display_name if display_name is not None else project_data.name

    replace_map: dict[str, str] = {
        "suap-binary-name": binary_name,
        "suap-binary-path": str(binary_path.absolute()),
        "suap-binary-dist-path": str(binary_dist_path.absolute()),
        "suap-display-name": display_name,
        "suap-icon-path": str(icon_path.absolute()),
        "suap-icon-file-name": icon_path.name,

        "suap-project-name": project_data.name,
        "suap-project-version": f"{semver.major}.{semver.minor}.{semver.patch}" \
            f".{semver.prerelease.split('.')[-1] if semver.prerelease is not None else 0}",
        "suap-project-description": project_data.description,

        "suap-app-capabilities-macro": generate_app_capabilities_macro(
            mime_types,
            templates_path,
            binary_name,
            display_name,
            icon_path,
            project_data,
            uninstall = False,
        ),
        "suap-app-capabilities-uni-macro": generate_app_capabilities_macro(
            mime_types,
            templates_path,
            binary_name,
            display_name,
            icon_path,
            project_data,
            uninstall = True,
        ),
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

    logger.info("Done making NSIS installer, installer executable should be in dist.")

def generate_app_capabilities_macro(
    mime_types: list[MimeType],
    templates_path: Path,
    binary_name: str,
    display_name: str,
    icon_path: Path,
    project_data: ProjectData,
    uninstall: bool,
) -> str:
    if len(mime_types) == 0:
        return ""

    app_capabilities_template_path = templates_path.joinpath(
        "nsis_app_capabilities_uni_macro.nsi" if uninstall else "nsis_app_capabilities_macro.nsi"
    )

    with open(app_capabilities_template_path, mode = "r") as file:
        app_capabilities_macro_string = file.read()

    file_associations_and_types_lines = []

    for mime_type in mime_types:
        file_extension = mime_type.get_file_extension()

        project_name = project_data.name

        if file_extension is None:
            logger.warning(f"Mime type '{mime_type.mime_type_string}' not found, skipping...")
            continue

        if not uninstall:
            file_associations_and_types_lines.append(
                f'WriteRegStr HKCR "Applications\\{binary_name}.exe\\SupportedTypes" "{file_extension}" ""'
            )

            file_associations_and_types_lines.append(
                f'WriteRegStr HKCR "{file_extension}\\OpenWithProgIds" "Cloudy.{project_name}.1" ""'
            )

            file_associations_and_types_lines.append(
                f'WriteRegStr HKLM "SOFTWARE\\Cloudy\\{project_name}\\Capabilities\\FileAssociations" "{file_extension}" "Cloudy.{project_name}.1"'
            )

        else:
            file_associations_and_types_lines.append(
                f'DeleteRegValue HKCR "Applications\\{binary_name}.exe\\SupportedTypes" "{file_extension}"'
            )

            file_associations_and_types_lines.append(
                f'DeleteRegValue HKCR "{file_extension}\\OpenWithProgIds" "Cloudy.{project_name}.1"'
            )

    replace_map: dict[str, str] = {
        "suap-binary-name": binary_name,
        "suap-display-name": display_name,
        "suap-icon-file-name": icon_path.name,

        "suap-project-name": project_data.name,
        "suap-project-description": project_data.description,

        "suap-file-associations-and-types-macro": "\n".join(file_associations_and_types_lines),
    }

    for (suap_key, value) in replace_map.items():
        app_capabilities_macro_string = app_capabilities_macro_string.replace(
            f"{{{suap_key}}}", value
        )

    formatted_macro_string = "".join([
        f"    {line}" for line in app_capabilities_macro_string.splitlines(keepends = True)
    ])

    logger.debug(
        f"Generated and formatted app capabilities macro: \n{formatted_macro_string}"
    )

    return formatted_macro_string