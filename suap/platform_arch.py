from enum import StrEnum

__all__ = ()

class PlatformArch(StrEnum):
    X86_64 = "x86_64"
    """
    64 bit extension of x86
    """
    AARCH64 = "aarch64"
    """
    64 bit ARM

    Also known as 'arm64' if you follow Microslop.
    """