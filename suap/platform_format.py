from enum import StrEnum

__all__ = ()

class PlatformFormat(StrEnum):
    LINUX = "linux"

    WINDOWS = "windows"
    WINDOWS_BINARY = "windows-bin"
    WINDOWS_SETUP = "windows-setup"

    MACOS = "macos"
