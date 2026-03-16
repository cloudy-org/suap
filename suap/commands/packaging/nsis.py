from typing import Optional

import logging
from typer import Exit
from pathlib import Path

from ...mime_type import MimeType
from ...projects import ProjectData
from ...formats import make_nsis_installer
from ...templating import Template, Key

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

    installer_script_template = Template("nsis_installer_script.nsi")

    semver = project_data.version

    binary_name_key = Key(name = "binary-name", value = binary_name)

    display_name_key = Key(
        name = "display-name",
        value = display_name if display_name is not None else project_data.name
    )

    icon_file_name_key = Key(name = "icon-file-name", value = icon_path.name)

    installer_script_string = installer_script_template.format(
        keys = (
            binary_name_key,
            Key(name = "binary-path", value = str(binary_path.absolute())),
            Key(name = "binary-dist-path", value = str(binary_dist_path.absolute())),

            display_name_key,

            Key(name = "icon-path", value = str(icon_path.absolute())),
            icon_file_name_key,

            Key(name = "project-name", value = project_data.name),
            Key(
                name = "project-version",
                value = f"{semver.major}.{semver.minor}.{semver.patch}" \
                    f".{semver.prerelease.split('.')[-1] if semver.prerelease is not None else 0}"
            ),
            Key(name = "project-description", value = project_data.description),

            Key(
                name = "app-capabilities-macro",
                value = generate_app_capabilities_macro(
                    mime_types,
                    binary_name_key,
                    display_name_key,
                    icon_file_name_key,
                    project_data,
                    uninstall = False,
                )
            ),
            Key(
                name = "app-capabilities-uni-macro",
                value = generate_app_capabilities_macro(
                    mime_types,
                    binary_name_key,
                    display_name_key,
                    icon_file_name_key,
                    project_data,
                    uninstall = True,
                )
            ),
        )
    )

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
    binary_name_key: Key,
    display_name_key: Key,
    icon_file_name_key: Key,
    project_data: ProjectData,
    uninstall: bool,
) -> str:
    if len(mime_types) == 0:
        return ""

    template_name = "nsis_app_capabilities_macro.nsi"

    if uninstall:
        template_name = "nsis_app_capabilities_uni_macro.nsi"

    app_capabilities_template = Template(template_name)

    file_associations_and_types_lines = []

    for mime_type in mime_types:
        file_extension = mime_type.get_file_extension()

        project_name = project_data.name

        if file_extension is None:
            logger.warning(f"Mime type '{mime_type.mime_type_string}' not found, skipping...")
            continue

        if not uninstall:
            file_associations_and_types_lines.append(
                f'WriteRegStr HKCR "Applications\\{binary_name_key.name}.exe\\SupportedTypes" "{file_extension}" ""'
            )

            file_associations_and_types_lines.append(
                f'WriteRegStr HKCR "{file_extension}\\OpenWithProgIds" "Cloudy.{project_name}.1" ""'
            )

            file_associations_and_types_lines.append(
                f'WriteRegStr HKLM "SOFTWARE\\Cloudy\\{project_name}\\Capabilities\\FileAssociations" "{file_extension}" "Cloudy.{project_name}.1"'
            )

        else:
            file_associations_and_types_lines.append(
                f'DeleteRegValue HKCR "Applications\\{binary_name_key.name}.exe\\SupportedTypes" "{file_extension}"'
            )

            file_associations_and_types_lines.append(
                f'DeleteRegValue HKCR "{file_extension}\\OpenWithProgIds" "Cloudy.{project_name}.1"'
            )

    app_capabilities_macro_string = app_capabilities_template.format(
        keys = (
            binary_name_key,
            display_name_key,
            icon_file_name_key,
            Key("project-name", project_data.name),
            Key("project-description", project_data.description),
            Key("file-associations-and-types-macro", value = "\n".join(file_associations_and_types_lines)),
        )
    )

    formatted_macro_string = "".join([
        f"    {line}" for line in app_capabilities_macro_string.splitlines(keepends = True)
    ])

    logger.debug(
        f"Generated and formatted app capabilities macro: \n{formatted_macro_string}"
    )

    return formatted_macro_string