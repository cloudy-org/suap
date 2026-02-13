from typing import TypedDict

__all__ = (
    "ConfigData",
)

CargoProjectData = TypedDict(
    "CargoProjectData",
    {
        "bin-crate": str
    }
)

class ProjectData(TypedDict):
    cargo: CargoProjectData

class ConfigData(TypedDict):
    version: int
    project: ProjectData