from typing import Annotated, Optional

import logging
from typer import Option, Typer

from .logger import LogFormatter

from .version import version_callback
from .package import app as package_app

app = Typer(
    pretty_exceptions_show_locals = False
)
app.add_typer(package_app)

logger = logging.getLogger(__name__)

@app.callback()
def callback(
    version: Annotated[
        Optional[bool],
        Option(
            "--version",
            is_eager = True,
            callback = version_callback,
            help = "Shows suap version."
        )
    ] = None,
):
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(LogFormatter())

    logging.basicConfig(
        format = "[%(levelname)s] %(message)s",
        level = logging.DEBUG,
        handlers = [log_handler]
    )

@app.command(hidden = True) # WIP
def tools():
    ...

if __name__ == "__main__":
    app()