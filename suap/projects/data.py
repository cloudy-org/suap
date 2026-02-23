from semver import Version
from dataclasses import dataclass

__all__ = (
    "ProjectData",
)

@dataclass
class ProjectData:
    name: str
    version: Version
    description: str