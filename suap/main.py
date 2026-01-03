from typing import Annotated

from enum import StrEnum
from typer import Option, Typer

app = Typer()

class ProjectType(StrEnum):
    CARGO = "cargo"

class Platform(StrEnum):
    WINDOWS = "windows"
    MACOS = "macos"

@app.command()
def main(
    project: Annotated[ProjectType, Option()],
    platform: Annotated[Platform, Option()]
):
    print("WIP!")

if __name__ == "__main__":
    app()