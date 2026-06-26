import os

__all__ = ()

INSIDE_DOCKER = True if "SUAP_DOCKER" in os.environ else False