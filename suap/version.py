from typer import Exit

__all__ = ()

__version__ = "1.0.0"

def version_callback(value: bool):
    if not value:
        return

    print(f"Version: {__version__}")
    raise Exit(0)