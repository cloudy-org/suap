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

class ConfigData(TypedDict):
    version: int
    project: ConfigProjectData