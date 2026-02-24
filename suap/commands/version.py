import suap
from typer import Exit

__all__ = ()

def version_callback(value: bool):
    if not value:
        return

    print(f"Version: {suap.__version__}")
    raise Exit(0)