from typing import TypedDict

__all__ = (
    "ConfigData",
)

ConfigCargoProjectData = TypedDict(
    "ConfigCargoProjectData",
    {
        "bin-crate": str
    }
)

class ConfigProjectData(TypedDict):
    cargo: ConfigCargoProjectData

ConfigData = TypedDict(
    "ConfigData",
    {
        "version": int,
        "display-name": str,
        "icons": str,
        "mime_types": list[str],
        "project": ConfigProjectData
    }
)