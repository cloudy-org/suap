from typing import assert_never

from enum import StrEnum, IntFlag, auto

__all__ = ()

class PlatformFormat(IntFlag):
    LINUX_BIN = auto()

    WINDOWS_BIN = auto()
    WINDOWS_SETUP = auto()

    MACOS_BIN = auto()

    # all formats in platform
    LINUX = LINUX_BIN
    WINDOWS = WINDOWS_BIN | WINDOWS_SETUP
    MACOS = MACOS_BIN

class PlatformFormatOption(StrEnum):
    LINUX = "linux"

    WINDOWS = "windows"
    WINDOWS_BINARY = "windows-bin"
    WINDOWS_SETUP = "windows-setup"

    MACOS = "macos"

    def get_platform_format(self) -> PlatformFormat:
        # NOTE: I'm using a match statement so I can take advantage of type 
        # checking to perform exhaustiveness checking of the `PlatformFormatOption` enum.

        match self:
            case PlatformFormatOption.LINUX: return PlatformFormat.LINUX # noqa: E701
            case PlatformFormatOption.WINDOWS: return PlatformFormat.WINDOWS # noqa: E701
            case PlatformFormatOption.WINDOWS_BINARY: return PlatformFormat.WINDOWS_BIN # noqa: E701
            case PlatformFormatOption.WINDOWS_SETUP: return PlatformFormat.WINDOWS_SETUP # noqa: E701
            case PlatformFormatOption.MACOS: return PlatformFormat.MACOS # noqa: E701
            case _:
                assert_never(self)