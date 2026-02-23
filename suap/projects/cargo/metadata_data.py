from typing import TypedDict

__all__ = (
    "CargoMetadataData",
)

# https://doc.rust-lang.org/cargo/commands/cargo-metadata.html#json-format

class CargoMetadataPackagesData(TypedDict):
    name: str
    version: str
    description: str

class CargoMetadataData(TypedDict):
    packages: list[CargoMetadataPackagesData]